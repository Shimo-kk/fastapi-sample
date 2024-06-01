from sqlalchemy import Column, Integer, VARCHAR
from app.infrastructure.database.dto import BaseDto
from app.domain.category.category_entity import CategoryEntity


class CategoryDto(BaseDto):
    """
    カテゴリのDTOクラス

    Attributes:
        user_id: ユーザーID
        name: 名称
    """

    __tablename__ = "categories"

    user_id = Column(Integer, nullable=False)
    name = Column(VARCHAR(50), nullable=False, comment="名称")

    @staticmethod
    def from_entity(entity: CategoryEntity) -> "CategoryDto":
        return CategoryDto(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            user_id=entity.user_id,
            name=entity.name,
        )

    def to_entity(self) -> CategoryEntity:
        return CategoryEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            name=self.name,
        )
