from fastapi import Request, Response
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel
from app.core.environment import CSRF_KEY


class CsrfSettings(BaseModel):
    secret_key: str = CSRF_KEY
    cookie_samesite: str = "none"
    cookie_secure: bool = True


@CsrfProtect.load_config
def get_csrf_config() -> CsrfSettings:
    return CsrfSettings()


def generate_csrf(response: Response) -> str:
    csrf_protect: CsrfProtect = CsrfProtect()
    csrf_token, signed_token = csrf_protect.generate_csrf()
    csrf_protect.set_csrf_cookie(signed_token, response)
    return csrf_token


async def validate_csrf(request: Request):
    csrf_protect: CsrfProtect = CsrfProtect()
    await csrf_protect.validate_csrf(request)
