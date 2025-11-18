from app.repositories.user_repository import UsersRepository
from app.security.hash_manager import verify_password

def authenticate(db, username: str, password: str):
    user = UsersRepository.get_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    
    return user