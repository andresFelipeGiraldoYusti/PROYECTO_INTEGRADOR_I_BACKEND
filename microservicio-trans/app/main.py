# app/main.py
# app/main.py
from fastapi import FastAPI

from app.routes.verification_routes import router as verification_router
from app.routes.supplier_routes import router as supplier_router
from app.routes.product_type_routes import router as product_type_router
from app.routes.risk_policy_routes import router as risk_policy_router
from app.routes.transaction_query_routes import router as transaction_query_router

from app.db.session import Base, engine

app = FastAPI(title="Transaction Verification Service", root_path="/auth")

# Solo el router de verification lleva prefix aquí:
app.include_router(verification_router, prefix="/verification", tags=["verification"])

# Estos ya tienen prefix dentro del archivo, NO lo repitas:
app.include_router(supplier_router)
app.include_router(product_type_router)
app.include_router(risk_policy_router)
app.include_router(transaction_query_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


@app.on_event("startup")
def on_startup():
    print(">>> Verificando/creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print(">>> Tablas listas.")
