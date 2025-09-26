# Antes
# from pydantic import BaseSettings

# Ahora
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_USER: str = os.getenv("MYSQL_USER", "root")
    DB_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    DB_HOST: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("MYSQL_PORT", 3306))
    DB_NAME: str = os.getenv("MYSQL_DB", "proyecto_integrador")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "mysecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        if self.DB_PASSWORD:
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            return f"mysql+pymysql://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
