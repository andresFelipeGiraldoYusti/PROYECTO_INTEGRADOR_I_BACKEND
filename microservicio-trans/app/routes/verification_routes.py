from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.verification_schema import VerificationResponse
from app.controllers.verification_controller import verify_transaction_controller
from app.schemas.verification_schema import TransactionVerificationRequest
from app.models.transactions import Transactions, MFAStatus, VerificationStatus
import httpx

router = APIRouter()

AUTH_SERVICE_URL = "http://microservicio-auth:8001"

@router.post("/transactions", response_model=VerificationResponse)
def verify_transaction_endpoint(
    data: TransactionVerificationRequest,
    db: Session = Depends(get_db),
):
    return verify_transaction_controller(data, db)



#================= Additional Endpoint for TOTP Verification ==================#

@router.post("/verify_transaction_totp")
async def verify_transaction_totp(tx_id: int, jwt: str, totp_code: str, db: Session = Depends(get_db)):
    tx = db.query(Transactions).filter(Transactions.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if tx.mfa_status != MFAStatus.PENDING:
        raise HTTPException(status_code=400, detail="Transaction MFA not in PENDING state")

    headers = {"Authorization": f"Bearer {jwt}"} if jwt else {}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(
                f"{AUTH_SERVICE_URL}/totp/verify_totp?totp_code={totp_code}",
                headers=headers
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Unable to reach auth service")

    print("Response from auth service:", resp.status_code, resp.text)
    
    try:
        data = resp.json()
    except ValueError:
        data = {}

    if resp.status_code != 200 or not data.get("is_valid", False):
        msg = data.get("message") or data.get("error") or resp.text
        raise HTTPException(status_code=400, detail=f"TOTP verification failed: {msg}")

    # Verificación exitosa: usar valores válidos del enum
    tx.mfa_status = MFAStatus.APPROVED
    tx.verification_status = VerificationStatus.SUCCESS

    db.add(tx)
    db.commit()
    db.refresh(tx)

    return {"status": "SUCCESS", "transaction_id": tx.id, "message": data.get("message")}