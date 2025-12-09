from typing import Optional, List
import requests
from app.test import user_data

USER_SERVICE_URL = "http://microservicio-auth:8001"

def get_user_by_id(user_id: int) -> Optional[dict]:
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=5)
        
        if response.status_code == 200:
            return response.json()
        
        return None
    
    except requests.RequestException:
        return None


def get_user_by_username(username: str) -> Optional[dict]:
    for u in user_data():
        if u["username"].lower() == username.lower():
            return u
    return None


def find_users_by_full_name(name_substring: str) -> List[dict]:
    name_substring = name_substring.lower()
    return [
        u for u in user_data()
        if name_substring in u["full_name"].lower()
    ]