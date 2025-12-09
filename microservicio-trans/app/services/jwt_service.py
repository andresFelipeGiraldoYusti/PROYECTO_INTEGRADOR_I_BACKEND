# app/services/jwt_service.py
from typing import Optional, Dict
from jose import jwt, JWTError

from core.config import settings  # ya tienes SECRET_KEY y ALGORITHM


def decode_access_token(token: str) -> Optional[Dict]:
    """
    {
        "sub": "1",
        "exp": 1765246522,
        "iat": 1765244722
    }
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        # Opcional: aseguramos que tenga las claves que esperas
        if not isinstance(payload, dict):
            return None

        for key in ("sub", "exp", "iat"):
            if key not in payload:
                return None

        return payload

    except JWTError:
        # Incluye tokens expirados, mal firmados, mal formados, etc.
        return None
