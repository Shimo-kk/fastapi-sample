from fastapi import APIRouter, Request, Response
from app.config.dependency import dependency_injector
from app.application.model import DefaultModel
from app.application.model.auth_model import SignUpModel, SignInModel
from app.presentation.controller.auth_controller import AuthController

router = APIRouter()

auth_contrller: AuthController = dependency_injector.get(AuthController)


@router.post("/signup", response_model=DefaultModel)
async def sign_up(request: Request, response: Response, data: SignUpModel):
    return auth_contrller.sign_up(data=data)


@router.post("/signin", response_model=DefaultModel)
async def sign_in(request: Request, response: Response, data: SignInModel):
    return auth_contrller.sign_in(response=response, data=data)


@router.get("/signout", response_model=DefaultModel)
async def sign_out(request: Request, response: Response):
    return auth_contrller.sign_out(response=response)
