from injector import inject, singleton
from app.application.model.task_model import TaskCreateModel, TaskReadModel, TaskUpdateModel
from app.application.interface.usecase.task_usecase import ITaskUsecase
from app.application.interface.database.database_handller import IDatabaseHandller
from app.domain.task.task_repository import ITaskRepository
from app.domain.task.task_entity import TaskEntity
from app.domain.user.user_repository import IUserRepository
from app.domain.user.user_entity import UserEntity
from app.core import exceptions


@singleton
class TaskUsecase(ITaskUsecase):
    """
    タスクユースケースの実装クラス

    Attributes:
        database_handller: データベースハンドラー
    """

    @inject
    def __init__(self, database_handller: IDatabaseHandller):
        self._database_handller = database_handller

    def create_task(self, user_email: str, data: TaskCreateModel) -> None:
        """
        タスクの作成

        Args:
            user_email: ユーザーのE-mailアドレス
            data: タスク作成モデル
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
                task_repository: ITaskRepository = repository_factory.get_repository(ITaskRepository)

                # E-mailでユーザーを取得
                user_entity: UserEntity = user_repository.find_by_email(email=user_email)

                # ユーザーが存在しない場合は例外を投げる
                if not user_entity:
                    raise exceptions.NotFoundError("ユーザーが存在しません。")

                # タスクのエンティティを作成
                new_task_entity: TaskEntity = TaskEntity.create(
                    user_id=user_entity.id,
                    title=data.title,
                    priority_id=data.priority_id,
                    category_id=data.category_id,
                    start_date=data.start_date,
                )

                # タスクを挿入
                task_repository.insert(entity=new_task_entity)

        except Exception:
            raise

    def get_all_task(self, user_email: str) -> list[TaskReadModel]:
        """
        カテゴリを全件取得

        Args:
            user_email: ユーザーのE-mailアドレス
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
                task_repository: ITaskRepository = repository_factory.get_repository(ITaskRepository)

                # E-mailでユーザーを取得
                user_entity: UserEntity = user_repository.find_by_email(email=user_email)

                # ユーザーが存在しない場合は例外を投げる
                if not user_entity:
                    raise exceptions.NotFoundError("ユーザーが存在しません。")

                # カテゴリを全件取得
                task_entity_list: list[TaskEntity] = task_repository.find_all(user_id=user_entity.id)

                # カテゴリ参照モデルへ変換
                result: list[TaskReadModel] = []
                for task_entity in task_entity_list:
                    task_read_model: TaskReadModel = TaskReadModel(
                        id=task_entity.id,
                        created_at=task_entity.created_at,
                        updated_at=task_entity.updated_at,
                        title=task_entity.title,
                        detail=task_entity.detail,
                        priority_id=task_entity.priority_id,
                        category_id=task_entity.category_id,
                        start_date=task_entity.start_date,
                        is_done=task_entity.is_done,
                    )
                    result.append(task_read_model)

                return result

        except Exception:
            raise

    def update_task(self, data: TaskUpdateModel) -> None:
        """
        タスクを更新

        Args:
            data: タスク更新モデル
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                task_repository: ITaskRepository = repository_factory.get_repository(ITaskRepository)

                # IDでタスクを取得
                task_entity: TaskEntity = task_repository.find_by_id(id=data.id)

                # タスクが存在しない場合は例外を投げる
                if not task_entity:
                    raise exceptions.NotFoundError("タスクが存在しません。")

                # タイトルを変更
                task_entity.change_title(title=data.title)

                # 詳細を変更
                task_entity.change_detail(detail=data.detail)

                # 優先度を変更
                task_entity.change_priority_id(priority_id=data.priority_id)

                # カテゴリを変更
                task_entity.change_category_id(category_id=data.category_id)

                # 開始日を変更
                task_entity.change_start_date(start_date=data.start_date)

                # タスクを更新
                task_repository.update(entity=task_entity)

        except Exception:
            raise

    def delete_task(self, id: int) -> None:
        """
        タスクを削除

        Args:
            id: 主キー
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                task_repository: ITaskRepository = repository_factory.get_repository(ITaskRepository)

                # タスクを削除
                task_repository.delete_by_id(id=id)

        except Exception:
            raise

    def done_task(self, id: int) -> None:
        """
        タスクを削除

        Args:
            id: 主キー
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                task_repository: ITaskRepository = repository_factory.get_repository(ITaskRepository)

                # IDでタスクを取得
                task_entity: TaskEntity = task_repository.find_by_id(id=id)

                # タスクが存在しない場合は例外を投げる
                if not task_entity:
                    raise exceptions.NotFoundError("タスクが存在しません。")

                # タスクを完了
                task_entity.done()

                # タスクを更新
                task_repository.update(entity=task_entity)

        except Exception:
            raise
