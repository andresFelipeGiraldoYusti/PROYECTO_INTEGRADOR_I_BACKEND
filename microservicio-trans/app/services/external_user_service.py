from typing import Optional, List
from app.test import user_data

def get_user_by_id(user_id: int) -> Optional[dict]:
    for u in user_data():
        if u["id"] == user_id:
            return u
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