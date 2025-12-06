from fastapi import APIRouter
from app.routers import user_routers, suppliers_routers, auth_routers, jwt_routers

router = APIRouter()
router.include_router(user_routers.router)
router.include_router(suppliers_routers.router)
router.include_router(auth_routers.router)
router.include_router(jwt_routers.router)

