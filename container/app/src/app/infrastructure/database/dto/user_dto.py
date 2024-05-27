from sqlalchemy import Column, VARCHAR
from app.infrastructure.database.dto import BaseDto
from app.domain.user.user_entity import UserEntity


class UserDto(BaseDto):
    """
    ユーザーのDTOクラス

    Attributes:
        name: 名称
        email: E-mailアドレス
        password: パスワード（ハッシュ済み）
    """

    __tablename__ = "users"

    name = Column(VARCHAR(50), nullable=False, comment="名称")
    email = Column(VARCHAR(255), unique=True, nullable=False, comment="E-mailアドレス")
    password = Column(VARCHAR(128), nullable=False, comment="パスワード")

    @staticmethod
    def from_entity(entity: UserEntity) -> "UserDto":
        return UserDto(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            name=entity.name,
            email=entity.email,
            password=entity.password,
        )

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            email=self.email,
            password=self.password,
        )
