from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "mysecret"
    LOGGING_DIR: str = "./logs"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

