# app/main.py
# app/main.py
from fastapi import FastAPI

from routes.verification_routes import router as verification_router
from routes.supplier_routes import router as supplier_router
from routes.product_type_routes import router as product_type_router
from routes.risk_policy_routes import router as risk_policy_router
from routes.transaction_query_routes import router as transaction_query_router
from routes.mfa_routes import router as mfa_router

from db.session import Base, engine
import models  # noqa: F401

app = FastAPI(title="Transaction Verification Service")

# Solo el router de verification lleva prefix aquí:
app.include_router(verification_router, prefix="/verification", tags=["verification"])

# Estos ya tienen prefix dentro del archivo, NO lo repitas:
app.include_router(supplier_router)
app.include_router(product_type_router)
app.include_router(risk_policy_router)
app.include_router(transaction_query_router)
app.include_router(mfa_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)




"""
VA DESPUÉS DE APP
@app.on_event("startup")
def on_startup():
    print(">>> Verificando/creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print(">>> Tablas listas.")
"""