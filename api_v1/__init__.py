from fastapi import APIRouter

from .products.views import router as products_router
from .auth.views import router as auth_router
from .auth.jwt_auth_views import router as jwt_router

auth_router.include_router(router=jwt_router)
router = APIRouter()
router.include_router(router=products_router, prefix="/products")
router.include_router(router=auth_router)
