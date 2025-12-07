import pyotp
import qrcode
import io
import base64

def generate_totp_secret() -> dict:
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=30)
    return {"secret": secret, "current_otp": totp.now()}

def generate_totp_qr_uri(id: str, issuer_name: str) -> str:
    secret = pyotp.random_base32()
    print(secret)
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=id, issuer_name=issuer_name)
    
    img = qrcode.make(uri)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    
    # Convertir a base64
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        'secret': secret,
        'uri': uri,
        'qr_code': f"data:image/png;base64,{img_str}"
    }

def verify_totp_secret(token: str, user_secret: str) -> dict:
    print(user_secret)
    totp = pyotp.TOTP(user_secret)
    is_valid = totp.verify(token)
    return {"is_valid": is_valid}