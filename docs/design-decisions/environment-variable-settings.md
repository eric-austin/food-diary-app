# Environment Variable and Settings Management

This document outlines how the application manages configuration settings using environment variables and Pydantic.

## Approach

We will use the `pydantic-settings` library to manage application configuration. This library provides a `BaseSettings` class that automatically reads settings from environment variables and `.env` files, while leveraging Pydantic's validation and type hinting capabilities.

This approach offers several advantages:
- **Centralized Configuration:** All settings defined in one place.
- **Type Safety:** Settings are automatically cast to the correct Python types (e.g., `int`, `bool`, `str`).
- **Validation:** Pydantic validators can be used to ensure settings have valid values.
- **Environment Variable Override:** Settings can be easily overridden by system environment variables, which is standard practice for deployment.
- **`.env` File Support:** Loads settings from a `.env` file during local development for convenience.
- **IDE Integration:** Type hints provide better autocompletion and static analysis.

## Implementation

1.  **Dependency:** Add `pydantic-settings` to `requirements.txt`:
    ```
    pydantic-settings>=2.0.0,<3.0.0
    ```

2.  **Settings Class (`app/config.py`):** Define a class that inherits from `pydantic_settings.BaseSettings`. Field names correspond to environment variable names (case-insensitive by default).

    ```python
    # Example: app/config.py
    from pydantic_settings import BaseSettings
    from pydantic import PostgresDsn, AnyHttpUrl
    from typing import Literal

    class Settings(BaseSettings):
        # Core settings
        APP_ENV: Literal['development', 'production', 'testing'] = 'development'
        SECRET_KEY: str  # No default, must be set in env

        # Database settings
        DATABASE_URL: PostgresDsn

        # Optional Settings with Defaults
        LOG_LEVEL: str = 'INFO'

        # Example for OAuth (Google)
        GOOGLE_CLIENT_ID: str | None = None
        GOOGLE_CLIENT_SECRET: str | None = None
        GOOGLE_REDIRECT_URI: AnyHttpUrl | None = None # Example validation

        # Example for Email Service (Resend)
        RESEND_API_KEY: str | None = None
        EMAIL_FROM_ADDRESS: str = "noreply@example.com" # Default from address

        class Config:
            # Specify the .env file location (relative to project root)
            env_file = '.env'
            env_file_encoding = 'utf-8'
            # Optional: Prefix for environment variables (e.g., FOOD_DIARY_DATABASE_URL)
            # env_prefix = 'FOOD_DIARY_'
            # Enable extra fields (useful if env has extra vars we don't define)
            extra = 'ignore' # or 'allow'

    # Instantiate the settings once
    settings = Settings()

    # Usage in other modules:
    # from app.config import settings
    # db_url = settings.DATABASE_URL
    # if settings.APP_ENV == 'development':
    #     print("Running in dev mode")
    ```

3.  **`.env` File:** Create a `.env` file in the project root for local development overrides. **Do not commit `.env` to version control.** Add it to `.gitignore`.

    ```dotenv
    # .env example
    APP_ENV=development
    SECRET_KEY=your_super_secret_development_key_here # Generate a real one
    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/food_diary_db

    # Development OAuth Credentials (if testing OAuth locally)
    GOOGLE_CLIENT_ID=your_dev_google_client_id.apps.googleusercontent.com
    GOOGLE_CLIENT_SECRET=your_dev_google_client_secret
    GOOGLE_REDIRECT_URI=http://localhost:5001/auth/google/callback

    # Development Email Credentials (if testing email locally)
    # RESEND_API_KEY=your_dev_resend_key
    # EMAIL_FROM_ADDRESS=dev-noreply@yourdomain.com
    ```

## Usage

Import the instantiated `settings` object from `app/config.py` wherever configuration values are needed. Pydantic ensures that the settings are loaded and validated only once when the application starts. 