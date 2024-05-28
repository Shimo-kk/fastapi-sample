from abc import ABC, abstractmethod
from app.application.model.auth_model import SignUpModel, SignInModel


class IAuthUsecase(ABC):
    """
    認証ユースケースのインタフェース
    """

    @abstractmethod
    def sign_up(self, data: SignUpModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def sign_in(self, data: SignInModel) -> str:
        raise NotImplementedError
