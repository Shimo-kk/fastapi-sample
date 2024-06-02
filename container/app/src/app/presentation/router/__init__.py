from fastapi import APIRouter
from app.presentation.router import csrf_router
from app.presentation.router import auth_router
from app.presentation.router.v1 import category_router
from app.presentation.router.v1 import priority_router
from app.presentation.router.v1 import task_router


v1_router = APIRouter()
v1_router.include_router(priority_router.router, prefix="/priority", tags=["priority"])
v1_router.include_router(category_router.router, prefix="/category", tags=["category"])
v1_router.include_router(task_router.router, prefix="/task", tags=["task"])

api_router = APIRouter()
api_router.include_router(csrf_router.router, prefix="/csrf", tags=["csrf"])
api_router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
api_router.include_router(v1_router, prefix="/v1")
