from fastapi import APIRouter
from app.presentation.router import csrf_router
from app.presentation.router import auth_router
from app.presentation.router.v1 import category_router

v1_router = APIRouter()
v1_router.include_router(category_router.router, prefix="/category", tags=["category"])

api_router = APIRouter()
api_router.include_router(csrf_router.router, prefix="/csrf", tags=["csrf"])
api_router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
api_router.include_router(v1_router, prefix="/v1")
