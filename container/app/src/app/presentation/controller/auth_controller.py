from fastapi import Response, HTTPException, status
from injector import inject, singleton
from app.application.interface.usecase.auth_usecase import IAuthUsecase
from app.application.model import DefaultModel
from app.application.model.auth_model import SignUpModel, SignInModel
from app.core import exceptions
from app.presentation.auth import auth_jwt


@singleton
class AuthController:
    """
    認証コントローラークラス
    """

    @inject
    def __init__(self, auth_usecase: IAuthUsecase):
        self._auth_usecase = auth_usecase

    def sign_up(self, data: SignUpModel) -> DefaultModel:
        """
        サインアップ

        Args:
            data: サインインモデル

        Returns:
            DefaultModel: デフォルトのレスポンス
        """
        try:
            # ユースケース実行
            self._auth_usecase.sign_up(data=data)

            return DefaultModel(message="サインアップしました。")

        except exceptions.AlreadyExistsError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def sign_in(self, response: Response, data: SignInModel) -> DefaultModel:
        """
        サインイン

        Args:
            response: レスポンス
            data: サインインモデル

        Returns:
            DefaultModel: デフォルトのレスポンス
        """
        try:
            # ユースケース実行
            email: str = self._auth_usecase.sign_in(data=data)

            # JWTトークン生成
            token = auth_jwt.encode_jwt(subject=email)

            # JWTトークンをCookieに設定
            response.set_cookie(
                key="access_token", value=f"Bearer {token}", httponly=True, samesite="none", secure=True
            )

            return DefaultModel(message="サインインしました。")

        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except exceptions.BadRequestError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def sign_out(self, response: Response):
        """
        サインアウト

        Args:
            response: レスポンス
        """
        response.set_cookie(key="access_token", value="", httponly=True, samesite="none", secure=True)
        return DefaultModel(message="サインアウトしました。")
