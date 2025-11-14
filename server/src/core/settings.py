from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "100.92.64.105"
    db_port: int = 5432
    db_name: str = "lava"

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    log_dir: str = "./logs"
    
    jwt_secret: str = "4ca575fa42b3b84b613e4c8792a6e3341320b41a22103a6202871e7f1346163c"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

