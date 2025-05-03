import uuid
import base64
import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, LargeBinary, Index, CheckConstraint,
    TypeDecorator
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # Keep for potential PG use
from sqlalchemy.orm import relationship
# We'll use uuid6 library for UUIDv7 generation
# pip install uuid6
import uuid6

from . import Base

# Custom TypeDecorator for storing UUID as BINARY(16) in SQLite
class UuidAsBinary(TypeDecorator):
    """Stores Python UUID objects as BINARY(16) in the database.

    Handles conversion between Python UUID objects and their
    byte representations.
    """
    impl = LargeBinary(16)
    cache_ok = True # Enable caching for this type wrapper

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            raise TypeError("value must be a UUID object")
        # Convert UUID to bytes for storage
        return value.bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, bytes):
            # Ensure we received bytes back
            raise TypeError("value must be bytes")
        # Convert bytes back to UUID
        return uuid.UUID(bytes=value)

# Helper function to generate Base32 public ID from UUID
# We'll call this in our application logic before saving a new user
def generate_public_id(pk_id: uuid.UUID) -> str:
    """Generates a URL-safe Base32 encoded string from the first 8 bytes of a UUID."""
    # Take first 8 bytes
    first_8_bytes = pk_id.bytes[:8]
    # Encode in Base32 and remove padding
    encoded = base64.b32encode(first_8_bytes).decode('utf-8').rstrip('=')
    return encoded


class User(Base):
    __tablename__ = 'users'

    # Use the custom UuidAsBinary type for the primary key
    id: uuid.UUID = Column(UuidAsBinary, primary_key=True, default=uuid6.uuid7)
    # Public ID will be generated *before* saving the user object in application code
    public_id: str = Column(String(13), unique=True, index=True, nullable=False)

    email: str | None = Column(String, unique=True, index=True, nullable=True)
    password_hash: str | None = Column(String, nullable=True) # Store hash, not plaintext
    first_name: str | None = Column(String(100), nullable=True)
    last_name: str | None = Column(String(100), nullable=True)

    is_anonymous: bool = Column(Boolean, default=False, nullable=False, index=True)
    # Email verification fields
    email_verified: bool = Column(Boolean, default=False, nullable=False)
    email_verification_token: str | None = Column(String, unique=True, nullable=True, index=True)
    email_verification_token_expires_at: datetime.datetime | None = Column(DateTime, nullable=True)

    last_active_at: datetime.datetime = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False
    )
    created_at: datetime.datetime = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False
    )
    updated_at: datetime.datetime = Column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.UTC),
        onupdate=lambda: datetime.datetime.now(datetime.UTC),
        nullable=False
    )

    # Relationships (add as needed later)
    # settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    # food_entries = relationship("FoodEntry", back_populates="user", cascade="all, delete-orphan")

    # Add multi-column index for cleanup query
    __table_args__ = (
        Index('ix_users_anon_cleanup', 'is_anonymous', 'last_active_at'),
        # Ensure registered users have an email
        CheckConstraint(
            "NOT(is_anonymous = false AND email IS NULL)",
            name="ck_user_registered_email"
        ),
        # Ensure registered users have a password hash
         CheckConstraint(
            "NOT(is_anonymous = false AND password_hash IS NULL)",
            name="ck_user_registered_password"
        ),
        # Index for email verification token lookup
        Index('ix_users_email_verification_token', 'email_verification_token', unique=True),
    )

    def __repr__(self):
        return f"<User(id={self.id!r}, public_id={self.public_id!r}, email={self.email!r}, is_anonymous={self.is_anonymous})>" 