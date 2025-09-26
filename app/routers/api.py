from fastapi import APIRouter
from app.routers import user_routers

router = APIRouter()
router.include_router(user_routers.router)
