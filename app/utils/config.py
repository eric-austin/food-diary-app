from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    # app configuration
    APP_ENV: Literal["development", "production"] = "development"
    APP_SECRET_KEY: str
    # resend email configuration
    RESEND_API_KEY: str
    # database configuration
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()