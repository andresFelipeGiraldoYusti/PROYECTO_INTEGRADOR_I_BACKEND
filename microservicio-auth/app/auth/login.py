from app.repositories.user_repository import UsersRepository
from app.security.hash_manager import verify_password
from app.security.jwt_manager import create_jwt_token

def authenticate(db, username: str, password: str):
    user = UsersRepository.get_by_email(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    
    return create_jwt_token(user.id)