# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import engine, Base
from app.routers.api import router

from app.models.users import Users
from app.models.transactions import Transactions
from app.models.risk_policies import RiskPolicies
from app.models.suppliers import Suppliers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de startup
    print("🔥 Servidor iniciado. Base de datos lista para conexiones.")
    yield
    # Código de shutdown
    print("💤 Servidor apagándose. Cerrando conexiones de DB.")

app = FastAPI(
    title="Backend Profesional con FastAPI",
    description="API REST para manejo de datos en base de datos",
    version="1.0.0",
    lifespan=lifespan
)

# Incluir todos los routers
app.include_router(router)

# Crear todas las tablas al iniciar la app
Base.metadata.create_all(bind=engine)

# Arranque con Uvicorn (solo si ejecutas directamente este archivo)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
