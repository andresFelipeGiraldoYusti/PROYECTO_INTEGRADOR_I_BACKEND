from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Decodificar JWT y retornar datos del usuario
def verify_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload  # contiene sub, roles, email, etc.
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
