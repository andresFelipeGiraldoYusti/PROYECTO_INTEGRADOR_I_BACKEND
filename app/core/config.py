# Antes
# from pydantic import BaseSettings

# Ahora
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

import os
from pydantic_settings import BaseSettings # Asumiendo que usas pydantic-settings

class Settings(BaseSettings):
    # --- Configuración de PostgreSQL ---
    DB_USER: str = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "root")
    DB_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    DB_NAME: str = os.getenv("POSTGRES_DB", "postgres")
    
    # --- Configuración de JWT (sin cambios) ---
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 7))
    APP_NAME: str = os.getenv("APP_NAME", "MiApp")
    APP_DOMAIN: str = os.getenv("APP_DOMAIN", "https://miapp.com")
    API_DOMAIN: str = os.getenv("API_DOMAIN", "https://api.miapp.com")

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        # El prefijo cambia a 'postgresql' y usamos el driver 'psycopg' (o 'asyncpg' si fuera asíncrono)
        # Usamos 'postgresql+psycopg' (o 'postgresql+psycopg2') para la conexión síncrona con SQLAlchemy
        
        # PostgreSQL generalmente requiere contraseña
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
settings = Settings()
