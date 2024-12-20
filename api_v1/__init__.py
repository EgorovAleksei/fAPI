from fastapi import APIRouter

from .products.views import router as products_router
from .auth.views import router as auth_router

router = APIRouter()
router.include_router(router=products_router, prefix="/products")
router.include_router(router=auth_router)
