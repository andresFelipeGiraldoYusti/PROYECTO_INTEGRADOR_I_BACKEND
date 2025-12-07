# app/core/roles.py

from fastapi import HTTPException, Depends
from app.core.security import verify_jwt

def require_role(required_role: str):
    def role_checker(payload: dict = Depends(verify_jwt)):
        roles = payload.get("roles", [])
        if required_role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Acceso denegado. Requiere rol: {required_role}"
            )
        return payload
    return role_checker
