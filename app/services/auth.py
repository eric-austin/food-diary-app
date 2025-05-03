import uuid
import datetime
from typing import Any
import uuid6

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.requests import Request

from app.models.user import User, generate_public_id
from app.utils.database import db_session_manager

# Define the type for the auth context we store in the request scope
# Using a simple UUID for now, could be a dataclass later if more info needed
AuthContext = uuid.UUID | None

async def ensure_user_context(
    request: Request,
    session: dict
) -> None:
    """Beforeware function to ensure a user context exists for every request.

    Checks for a public_id in the session cookie. If found and valid,
    loads the user and updates last_active_at. If not found or invalid,
    creates a new anonymous user, stores their public_id in the session,
    and sets the user context.

    Stores the user's primary key (UUID) in request.scope['auth'].
    Manages its own database session using db_session_manager.
    """
    public_id = session.get('public_id')
    user_pk: uuid.UUID | None = None

    # Manage session explicitly within the function
    async with db_session_manager() as db:
        user: User | None = None
        if public_id:
            # Try to find user by public_id from session
            stmt = select(User).where(User.public_id == public_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                # User found, update last active time
                user.last_active_at = datetime.datetime.now(datetime.UTC)
                db.add(user)
                # Commit will happen automatically at the end of db_session_manager block
                user_pk = user.id
                print(f"Found user by session public_id: {public_id}, user_pk: {user_pk}") # Debug
            else:
                # Public ID in session but no matching user (stale cookie?)
                print(f"Stale public_id in session: {public_id}, creating new anonymous user.") # Debug
                public_id = None # Force creation of new user
                # We modify the session object directly, Starlette middleware handles saving it
                session.pop('public_id', None) # Clear stale ID from session

        if not user_pk:
            # No valid user found yet, create a new anonymous one
            new_pk = uuid6.uuid7()
            new_public_id = generate_public_id(new_pk)

            new_user = User(
                id=new_pk,
                public_id=new_public_id,
                is_anonymous=True,
            )
            db.add(new_user)
            # Commit will happen automatically
            # Session is a dict-like object
            session['public_id'] = new_public_id
            user_pk = new_pk
            print(f"Created new anonymous user: {new_public_id}, user_pk: {user_pk}") # Debug

    # Store the user's primary key in the request scope for handlers to use
    # This needs to be done *outside* the db session context if db_session_manager closes it
    request.scope['auth'] = user_pk
    print(f"Auth context set in request.scope['auth']: {user_pk}") # Debug
