from fastapi import APIRouter
from app.routers import user_routers
from app.routers import suppliers_routers
from app.routers import auth_routers

router = APIRouter()
router.include_router(user_routers.router)
router.include_router(suppliers_routers.router)
router.include_router(auth_routers.router)
