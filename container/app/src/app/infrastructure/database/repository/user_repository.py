from sqlalchemy.orm.session import Session
from app.domain.user.user_entity import UserEntity
from app.domain.user.user_repository import IUserRepository
from app.infrastructure.database.dto.user_dto import UserDto


class UserRepository(IUserRepository):
    """
    ユーザーのリポジトリクラス

    Attributes:
        db_session: DBセッション
    """

    def __init__(self, session: Session):
        self._db_session: Session = session

    def insert(self, entity: UserEntity) -> UserEntity:
        """
        ユーザーの挿入

        Args:
            entity: 挿入するユーザーのエンティティ
        Returns:
            UserEntity: 挿入したユーザーのエンティティ
        """
        user_dto: UserDto = UserDto.from_entity(entity)
        self._db_session.add(user_dto)
        self._db_session.flush()
        self._db_session.refresh(user_dto)

        result: UserEntity = user_dto.to_entity()
        return result

    def not_exists(self, email: str) -> bool:
        """
        存在していないか確認

        Args:
            email: E-mailアドレス
        Returns:
            bool: 存在していない場合、True
        """
        user_dto: UserDto = self._db_session.query(UserDto).filter_by(email=email).first()
        if user_dto:
            return False

        return True

    def find_by_id(self, id: int) -> UserEntity:
        """
        主キーでの取得

        Args:
            id: 主キー
        Returns:
            UserEntity: 取得したユーザーのエンティティ
        """
        user_dto: UserDto = self._db_session.query(UserDto).filter_by(id=id).first()
        if not user_dto:
            return None

        result: UserEntity = user_dto.to_entity()
        return result

    def find_by_email(self, email: str) -> UserEntity:
        """
        E-mailアドレスでの取得

        Args:
            email: E-mailアドレス
        Returns:
            UserEntity: 挿入したユーザーのエンティティ
        """
        user_dto: UserDto = self._db_session.query(UserDto).filter_by(email=email).first()
        if not user_dto:
            return None

        result: UserEntity = user_dto.to_entity()
        return result

    def update(self, entity: UserEntity) -> UserEntity:
        """
        ユーザーの更新

        Args:
            entity: 更新するユーザーのエンティティ
        Returns:
            UserEntity: 更新したユーザーのエンティティ
        """
        user_dto: UserDto = self._db_session.query(UserDto).filter_by(id=entity.id).first()
        user_dto.name = entity.name
        self._db_session.flush()

        result: UserEntity = user_dto.to_entity()
        return result

    def delete_by_id(self, id: int) -> None:
        """
        主キーでの削除

        Args:
            id: 主キー
        """
        self._db_session.query(UserDto).filter_by(id=id).delete()

        return None
