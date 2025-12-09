# app/main.py
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine, Base
from app.routers.api import router

from app.models.users import Users
from app.models.totp import TOTP

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔥 Servidor iniciado. Base de datos lista para conexiones.")
    yield
    print("💤 Servidor apagándose. Cerrando conexiones de DB.")

app = FastAPI(
    title="Backend Profesional con FastAPI",
    description="API REST para manejo de datos en base de datos",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/auth"
)

# ======== CORS ========
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ========================

# Incluir todos los routers
app.include_router(router)

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)