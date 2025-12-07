from fastapi import APIRouter
from app.routers import user_routers, auth_routers, totp_routers

router = APIRouter()
router.include_router(user_routers.router)
router.include_router(auth_routers.router)
router.include_router(totp_routers.router)