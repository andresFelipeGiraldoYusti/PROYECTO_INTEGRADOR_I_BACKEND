# app/main.py
from fastapi import FastAPI
from routes.verification_routes import router as verification_router

app = FastAPI(title="Transaction Verification Service")

app.include_router(
    verification_router,
    prefix="/verification",
    tags=["verification"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
