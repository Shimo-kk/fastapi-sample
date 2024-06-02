from fastapi import Request, HTTPException, status
from injector import inject, singleton
from app.application.interface.usecase.task_usecase import ITaskUsecase
from app.application.model import DefaultModel
from app.application.model.task_model import TaskCreateModel, TaskReadModel, TaskUpdateModel
from app.core import exceptions
from app.presentation.auth import auth_jwt


@singleton
class TaskController:
    """
    タスクコントローラークラス
    """

    @inject
    def __init__(self, task_usecase: ITaskUsecase):
        self._task_usecase = task_usecase

    def create_category(self, request: Request, data: TaskCreateModel) -> DefaultModel:
        """
        タスクを作成

        Args:
            request: リクエスト
            data: タスク作成モデル

        Returns:
            DefaultModel: デフォルトのレスポンス
        """
        try:
            # JWTトークンからSubjectを取得
            subject: str = auth_jwt.get_subject_from_cookie(request=request)

            # ユースケース実行
            self._task_usecase.create_task(user_email=subject, data=data)

            return DefaultModel(message="タスクを作成しました。")

        except exceptions.ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def get_all_task(self, request: Request) -> list[TaskReadModel]:
        """
        全てのタスクを取得

        Args:
            request: リクエスト

        Returns:
            list[TaskReadModel]: タスク参照モデルリスト
        """
        try:
            # JWTトークンからSubjectを取得
            subject: str = auth_jwt.get_subject_from_cookie(request=request)

            # ユースケース実行
            return self._task_usecase.get_all_task(user_email=subject)

        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def update_task(self, data: TaskUpdateModel) -> DefaultModel:
        """
        タスクを更新

        Args:
            data: タスク更新モデル

        Returns:
            DefaultModel: デフォルトのレスポンス
        """
        try:
            # ユースケース実行
            self._task_usecase.update_task(data=data)

            return DefaultModel(message="タスクを更新しました。")

        except exceptions.ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_category(self, id: int) -> DefaultModel:
        """
        タスクを削除

        Args:
            id: 主キー
        Returns:
            DefaultModel: デフォルトのレスポンス
        """
        try:
            self._task_usecase.delete_task(id=id)

            return DefaultModel(message="タスクを削除しました。")

        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def done_task(self, id: int) -> DefaultModel:
        """
        タスクを完了

        Args:
            id: 主キー
        Returns:
            DefaultModel: デフォルトのレスポンス
        """
        try:
            self._task_usecase.done_task(id=id)

            return DefaultModel(message="タスクを完了しました。")

        except exceptions.NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
