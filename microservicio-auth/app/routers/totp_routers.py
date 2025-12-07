from fastapi import APIRouter

from app.security.totp_manager import generate_totp_secret, generate_totp_qr_uri

router = APIRouter(prefix="/totp", tags=["TOTP"])

@router.post("/generate_totp")
async def generate_totp():
    try:
        return {"message": "TOTP generation endpoint"}
    except ValueError as e:
        return {"error": str(e)}