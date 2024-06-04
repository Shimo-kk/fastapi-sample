from fastapi import Request, HTTPException, status
from injector import inject, singleton
from app.application.interface.usecase.category_usecase import ICategoryUsecase
from app.application.model import DefaultModel
from app.application.model.category_model import CategoryCreateModel, CategoryReadModel, CategoryUpdateModel
from app.core import exceptions
from app.presentation.auth import auth_jwt


@singleton
class CategoryController:
    """
    カテゴリコントローラークラス
    """

    @inject
    def __init__(self, category_usecase: ICategoryUsecase):
        self._category_usecase = category_usecase

    def create_category(self, request: Request, data: CategoryCreateModel) -> DefaultModel:
        """
        カテゴリを作成

        Args:
            request: リクエスト
            data: カテゴリ作成モデル

        Returns:
            DefaultModel: デフォルトのレスポンス
        """
        try:
            # JWTトークンからSubjectを取得
            subject: str = auth_jwt.get_subject_from_cookie(request=request)

            # ユースケース実行
            self._category_usecase.create_category(user_email=subject, data=data)

            return DefaultModel(message="カテゴリを作成しました。")
        except exceptions.ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def get_all_category(self, request: Request) -> list[CategoryReadModel]:
        """
        全てのカテゴリを取得

        Args:
            request: リクエスト

        Returns:
            list[CategoryReadModel]: カテゴリ参照モデルリスト
        """
        try:
            # JWTトークンからSubjectを取得
            subject: str = auth_jwt.get_subject_from_cookie(request=request)

            # ユースケース実行
            return self._category_usecase.get_all(user_email=subject)

        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def update_category(self, data: CategoryUpdateModel) -> DefaultModel:
        """
        カテゴリを更新

        Args:
            data: カテゴリ更新モデル

        Returns:
            DefaultModel: デフォルトのレスポンス
        """
        try:
            # ユースケース実行
            self._category_usecase.update_category(data=data)

            return DefaultModel(message="カテゴリを更新しました。")

        except exceptions.ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_category(self, id: int) -> DefaultModel:
        """
        カテゴリを削除

        Args:
            id: 主キー
        Returns:
            DefaultModel: デフォルトのレスポンス
        """
        try:
            self._category_usecase.delete_category(id=id)

            return DefaultModel(message="カテゴリを削除しました。")

        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
