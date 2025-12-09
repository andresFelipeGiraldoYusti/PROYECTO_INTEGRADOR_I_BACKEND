# app/routes/mfa_routes.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from services.totp_proxy_service import verify_totp

router = APIRouter(prefix="/mfa", tags=["mfa"])

# Solo extrae el JWT, NO valida localmente
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/verify")
async def verify_totp_endpoint(
    token: str = Depends(oauth2_scheme),
    totp_code: str = ""
):
    """
    Reenvía el token y el TOTP al microservicio de autenticación.
    Este microservicio NO valida el TOTP por su cuenta.
    """
    return verify_totp(token, totp_code)
