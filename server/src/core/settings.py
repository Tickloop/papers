from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "0.0.0.0"
    db_port: int = 5432
    db_name: str = "lava"

    db_url: str = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    log_dir: str = "./logs"
    
    jwt_secret: str = "4ca575fa42b3b84b613e4c8792a6e3341320b41a22103a6202871e7f1346163c"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

