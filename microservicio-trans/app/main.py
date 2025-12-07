# app/main.py
from fastapi import FastAPI
from routes.verification_routes import router as verification_router

# 🔹 Importa Base y engine
from db.session import Base, engine

# 🔹 Importa modelos para que se registren en Base.metadata
import models  # noqa: F401  # Fuerza la carga de app/models/__init__.py

app = FastAPI(title="Transaction Verification Service")

# 👉 Verificar/crear tablas al iniciar la app
"""
@app.on_event("startup")
def on_startup():
    print(">>> Verificando/creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print(">>> Tablas listas.")
"""

app.include_router(
    verification_router,
    prefix="/verification",
    tags=["verification"],
)

if __name__ == "__main__":
    import uvicorn
    # Nota: si ejecutas desde la raíz del proyecto, mejor usar "app.main:app"
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
