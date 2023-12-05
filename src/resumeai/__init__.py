# src/resumeai/__init__.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HELICONE_API_KEY: str


settings = Settings()
