# app/security/jwt_dependency.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from services.jwt_service import decode_access_token

# Solo se usa para extraer el token del header Authorization: Bearer xxx
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def require_user(token: str = Depends(oauth2_scheme)):
    """
    Dependencia para proteger endpoints.
    """
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired JWT"
        )

    # Aquí NO usamos este usuario para reglas de negocio de riesgo;
    # solo confirmamos que el JWT es válido.
    return payload
