from app.application.usecase.auth_usecase import AuthUsecase
from app.application.model.auth_model import SignUpModel, SignInModel
from app.core import exceptions


def test_signup_ok(injector):
    """
    サインアップ OK
    """
    auth_usecase: AuthUsecase = injector.get(AuthUsecase)

    data: SignUpModel = SignUpModel(name="test user", email="test@example.com", password="testtest")

    try:
        auth_usecase.sign_up(data=data)

    except Exception:
        assert False


def test_signup_ng_already_exists(injector):
    """
    サインアップ NG
    """
    auth_usecase: AuthUsecase = injector.get(AuthUsecase)

    data: SignUpModel = SignUpModel(name="test user", email="test1@example.com", password="testtest")

    try:
        auth_usecase.sign_up(data=data)

    except exceptions.AlreadyExistsError:
        assert True
    except Exception:
        assert False


def test_signin_ok(injector):
    """
    サインイン OK
    """
    auth_usecase: AuthUsecase = injector.get(AuthUsecase)

    data: SignInModel = SignInModel(email="test1@example.com", password="testtest")

    try:
        auth_usecase.sign_in(data=data)

    except Exception:
        assert False


def test_signin_ng_not_found(injector):
    """
    サインイン NG
    """
    auth_usecase: AuthUsecase = injector.get(AuthUsecase)

    data: SignInModel = SignInModel(email="test@example.com", password="testtest")

    try:
        auth_usecase.sign_in(data=data)

    except exceptions.NotFoundError:
        assert True
    except Exception:
        assert False


def test_signin_ng_bad_request(injector):
    """
    サインイン NG
    """
    auth_usecase: AuthUsecase = injector.get(AuthUsecase)

    data: SignInModel = SignInModel(email="test1@example.com", password="testtesttest")

    try:
        auth_usecase.sign_in(data=data)

    except exceptions.BadRequestError:
        assert True
    except Exception:
        assert False
