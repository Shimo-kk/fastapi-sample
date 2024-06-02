from sqlalchemy import Column, VARCHAR
from app.infrastructure.database.dto import BaseDto
from app.domain.priority.priority_entity import PriorityEntity


class PriorityDto(BaseDto):
    """
    優先度のDTOクラス

    Attributes:
        name: 名称
    """

    __tablename__ = "priorities"

    name = Column(VARCHAR(50), nullable=False, comment="名称")

    @staticmethod
    def from_entity(entity: PriorityEntity) -> "PriorityDto":
        return PriorityDto(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            name=entity.name,
        )

    def to_entity(self) -> PriorityEntity:
        return PriorityEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
        )
