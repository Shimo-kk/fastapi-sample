from injector import inject, singleton
from app.application.model.category_model import CategoryCreateModel, CategoryReadModel, CategoryUpdateModel
from app.application.interface.usecase.category_usecase import ICategoryUsecase
from app.application.interface.database.database_handller import IDatabaseHandller
from app.domain.category.category_entity import CategoryEntity
from app.domain.category.category_repository import ICategoryRepository
from app.domain.user.user_repository import IUserRepository
from app.domain.user.user_entity import UserEntity
from app.core import exceptions


@singleton
class CategoryUsecase(ICategoryUsecase):
    """
    カテゴリユースケースの実装クラス

    Attributes:
        database_handller: データベースハンドラー
    """

    @inject
    def __init__(self, database_handller: IDatabaseHandller):
        self._database_handller = database_handller

    def create_category(self, user_email: str, data: CategoryCreateModel) -> None:
        """
        カテゴリの作成

        Args:
            user_email: ユーザーのE-mailアドレス
            data: カテゴリ作成モデル
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
                category_repository: ICategoryRepository = repository_factory.get_repository(ICategoryRepository)

                # E-mailでユーザーを取得
                user_entity: UserEntity = user_repository.find_by_email(email=user_email)

                # ユーザーが存在しない場合は例外を投げる
                if not user_entity:
                    raise exceptions.NotFoundError("ユーザーが存在しません。")

                # カテゴリのエンティティを作成
                new_category_entity: CategoryEntity = CategoryEntity.create(user_id=user_entity.id, name=data.name)

                # カテゴリを挿入
                category_repository.insert(entity=new_category_entity)

        except Exception:
            raise

    def get_all_category(self, user_email: str) -> list[CategoryReadModel]:
        """
        カテゴリを全件取得

        Args:
            user_email: ユーザーのE-mailアドレス
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
                category_repository: ICategoryRepository = repository_factory.get_repository(ICategoryRepository)

                # E-mailでユーザーを取得
                user_entity: UserEntity = user_repository.find_by_email(email=user_email)

                # ユーザーが存在しない場合は例外を投げる
                if not user_entity:
                    raise exceptions.NotFoundError("ユーザーが存在しません。")

                # カテゴリを全件取得
                category_entity_list: list[CategoryEntity] = category_repository.find_all(user_id=user_entity.id)

                # カテゴリ参照モデルへ変換
                result: list[CategoryReadModel] = []
                for category_entity in category_entity_list:
                    category_read_model: CategoryReadModel = CategoryReadModel(
                        id=category_entity.id,
                        created_at=category_entity.created_at,
                        updated_at=category_entity.updated_at,
                        name=category_entity.name,
                    )
                    result.append(category_read_model)

                return result

        except Exception:
            raise

    def update_category(self, data: CategoryUpdateModel) -> None:
        """
        カテゴリを更新

        Args:
            data: カテゴリ更新モデル
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                category_repository: ICategoryRepository = repository_factory.get_repository(ICategoryRepository)

                # IDでカテゴリを取得
                category_entity: CategoryEntity = category_repository.find_by_id(id=data.id)

                # カテゴリが存在しない場合は例外を投げる
                if not category_entity:
                    raise exceptions.NotFoundError("カテゴリが存在しません。")

                # カテゴリ名を変更
                category_entity.change_name(name=data.name)

                # カテゴリを更新
                category_repository.update(entity=category_entity)

        except Exception:
            raise

    def delete_category(self, id: int) -> None:
        """
        カテゴリを削除

        Args:
            id: 主キー
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                category_repository: ICategoryRepository = repository_factory.get_repository(ICategoryRepository)

                # カテゴリを削除
                category_repository.delete_by_id(id=id)

        except Exception:
            raise
