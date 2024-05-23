from sqlalchemy import Column, VARCHAR
from app.infrastructure.database.dto import BaseDto


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
