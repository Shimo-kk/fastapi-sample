from sqlalchemy.orm.session import Session
from app.domain.priority.priority_entity import PriorityEntity
from app.domain.priority.priority_repository import IPriorityRepository
from app.infrastructure.database.dto.priority_dto import PriorityDto


class PriorityRepository(IPriorityRepository):
    """
    優先度リポジトリの実装クラス

    Attributes:
        db_session: DBセッション
    """

    def __init__(self, session: Session):
        self._db_session: Session = session

    def find_all(self) -> list[PriorityEntity]:
        """
        全件取得

        Returns:
            list[PriorityEntity]: 取得した優先度のエンティティのリスト
        """
        priority_dto_list: list[PriorityDto] = self._db_session.query(PriorityDto).order_by(PriorityDto.id).all()

        result: list[PriorityEntity] = []
        for priority_dto in priority_dto_list:
            result.append(priority_dto.to_entity())

        return result

    def find_by_id(self, id: int) -> PriorityEntity:
        """
        主キーでの取得

        Args:
            id: 主キー
        Returns:
            PriorityEntity: 取得した優先度のエンティティ
        """
        priority_dto: PriorityDto = self._db_session.query(PriorityDto).filter_by(id=id).first()
        if not priority_dto:
            return None

        result: PriorityEntity = priority_dto.to_entity()
        return result
