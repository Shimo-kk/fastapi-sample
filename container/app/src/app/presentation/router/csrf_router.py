from fastapi import APIRouter, Request, Response
from app.presentation.auth import auth_csrf

router = APIRouter()


@router.get("")
async def get_csrf(request: Request, response: Response):
    token: str = auth_csrf.generate_csrf(response)
    return {"csrf_token": token}
