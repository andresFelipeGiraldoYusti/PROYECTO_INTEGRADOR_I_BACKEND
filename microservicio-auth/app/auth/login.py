from app.repositories.user_repository import UsersRepository
from app.security.hash_manager import verify_password
from app.security.jwt_manager import create_jwt_token
from jose import jwt, JWTError
from app.core.config import settings

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None

def authenticate(db, username: str, password: str):
    user = UsersRepository.get_by_email(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    
    return create_jwt_token(user.id)