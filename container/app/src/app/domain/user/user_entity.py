import os
import hashlib
from datetime import datetime
from app.core.exceptions import ValidationError
from app.domain import BaseEntity
from app.domain.user.user_validator import UserValidator


class UserEntity(BaseEntity):
    """
    ユーザーのエンティティクラス

    Attributes:
        _name: 名称
        _email: E-mailアドレス
        _password: パスワード（ハッシュ済み）
    """

    @staticmethod
    def create(name: str, email: str, password: str) -> "UserEntity":
        """
        エンティティの作成

        Args:
            name: 名称
            email: E-mailアドレス
            password: パスワード
        """

        # ユーザー名のバリデーション
        valid_message: str = UserValidator.validate_name(value=name)
        if valid_message:
            raise ValidationError(valid_message)

        # E-mailアドレスのバリデーション
        valid_message = UserValidator.validate_email(value=email)
        if valid_message:
            raise ValidationError(valid_message)

        # パスワードのバリデーション
        valid_message = UserValidator.validate_password(value=password)
        if valid_message:
            raise ValidationError(valid_message)

        # パスワードのハッシュ化
        salt: bytes = os.urandom(16)
        salt_hex: str = salt.hex()
        hashd: str = hashlib.sha256(salt + password.encode()).hexdigest()

        return UserEntity(name=name, email=email, password=f"{salt_hex}${hashd}")

    def __init__(
        self,
        id: int = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        name: str = "",
        email: str = "",
        password: str = "",
    ):
        """
        Args:
            id: 主キー
            created_at: 作成日時
            updated_at: 更新日時
            name: 名称
            email: E-mailアドレス
            password: パスワード
        """
        BaseEntity.__init__(self, id, created_at, updated_at)
        self._name: str = name
        self._email: str = email
        self._password: str = password

    def __eq__(self, o: object) -> bool:
        """
        Args:
            o: オブジェクト
        """
        return BaseEntity.__eq__(o)

    def verify_password(self, plain_pw: str) -> bool:
        """
        パスワードの検証

        Args:
            plain_pw: パスワード
        """
        salt_hex, stored_hash = self._password.split("$")
        salt = bytes.fromhex(salt_hex)
        provided_hash = hashlib.sha256(salt + plain_pw.encode()).hexdigest()
        return stored_hash == provided_hash

    def change_name(self, name: str):
        """
        ユーザー名の変更

        Args:
            name: ユーザー名
        """

        # ユーザー名のバリデーション
        valid_message: str = UserValidator.validate_name(value=name)
        if valid_message:
            raise ValidationError(valid_message)

        self._name = name

    def change_password(self, password: str):
        """
        パスワードの変更

        Args:
            password: パスワード
        """

        # パスワードのバリデーション
        valid_message = UserValidator.validate_password(value=password)
        if valid_message:
            raise ValidationError(valid_message)

        # パスワードのハッシュ化
        salt: bytes = os.urandom(16)
        salt_hex: str = salt.hex()
        hashd: str = hashlib.sha256(salt + password.encode()).hexdigest()

        self._password = f"{salt_hex}${hashd}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password
