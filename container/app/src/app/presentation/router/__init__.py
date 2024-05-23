from fastapi import APIRouter
from app.presentation.router import csrf_router

v1_router = APIRouter()

api_router = APIRouter()
api_router.include_router(csrf_router.router, prefix="/csrf", tags=["csrf"])
