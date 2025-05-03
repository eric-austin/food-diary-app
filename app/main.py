import os
from fasthtml.common import *
from starlette.requests import Request # Import Request for type hinting

# import config
from app.utils.config import settings
from app.services.auth import ensure_user_context, AuthContext
from app.utils.database import close_db
# Import the layout components
from app.utils.decorators import render_htmx_fragment_or_full_page

# check if the app is running in development mode
IS_DEVELOPMENT = settings.APP_ENV == "development"

# configure the beforeware to ensure a user context exists for every request
auth_middleware = Beforeware(
    ensure_user_context,
    skip=[r'/static/.*', r'.*\.css', r'.*\.js', r'/favicon\.ico']
)

# Configure based on environment
app, rt = fast_app(
    debug=IS_DEVELOPMENT,
    live=IS_DEVELOPMENT,
    before=auth_middleware,
    secret_key=settings.APP_SECRET_KEY,
)

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down and closing database connection pool...")
    await close_db()
    print("Database connection pool closed.")

@rt("/")
@render_htmx_fragment_or_full_page(title="Welcome to Food Diary AI")
async def get(request: Request):
    # Define and return only the specific content for the main area
    return (
        H1("Welcome to Food Diary AI"), # Heading for the main content
        P("Take pictures of your food, let AI track your diary."),
        P(A("Go to Changed Content", href="/change", hx_get="/change", hx_target="#main-content", hx_push_url="true"))
    )

# Route for /change
@rt("/change")
@render_htmx_fragment_or_full_page(title="Changed Page")
async def handle_change(request: Request):
    # Define and return only the specific content for the main area
    return (
        H1("Content Updated!"),
        P("This is the new content loaded via HTMX or direct navigation.")
    )

# Pass reload flag based on environment
serve(reload=IS_DEVELOPMENT)