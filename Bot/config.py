import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl 

class Settings(BaseSettings):
    BOT_TOKEN: str
    API_URL: HttpUrl = "http://localhost:8000"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
