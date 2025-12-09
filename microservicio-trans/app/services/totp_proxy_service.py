# app/services/totp_proxy_service.py

import requests

def verify_totp(token: str, code: str):
    
    url = "http://auth-service/auth/verify_totp"

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
        },
        params={
            "totp_code": code
        }
    )

    return response.json()
