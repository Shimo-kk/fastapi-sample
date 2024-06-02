from injector import inject, singleton
from app.application.model.priority_model import PriorityReadModel
from app.application.interface.usecase.priority_usecase import IPriorityUsecase
from app.application.interface.database.database_handller import IDatabaseHandller
from app.domain.priority.priority_entity import PriorityEntity
from app.domain.priority.priority_repository import IPriorityRepository


@singleton
class PriorityUsecase(IPriorityUsecase):
    """
    優先度ユースケースの実装クラス

    Attributes:
        database_handller: データベースハンドラー
    """

    @inject
    def __init__(self, database_handller: IDatabaseHandller):
        self._database_handller = database_handller

    def get_all_priority(self) -> list[PriorityReadModel]:
        """
        優先度を全件取得
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                priority_repository: IPriorityRepository = repository_factory.get_repository(IPriorityRepository)

                # 優先度を全件取得
                priority_entity_list: list[PriorityEntity] = priority_repository.find_all()

                # 優先度参照モデルへ変換
                result: list[PriorityReadModel] = []
                for priority_entity in priority_entity_list:
                    priority_read_model: PriorityReadModel = PriorityReadModel(
                        id=priority_entity.id,
                        created_at=priority_entity.created_at,
                        updated_at=priority_entity.updated_at,
                        name=priority_entity.name,
                    )
                    result.append(priority_read_model)

                return result

        except Exception:
            raise
