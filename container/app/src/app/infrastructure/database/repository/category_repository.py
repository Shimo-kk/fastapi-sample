from sqlalchemy.orm.session import Session
from app.domain.category.category_entity import CategoryEntity
from app.domain.category.category_repository import ICategoryRepository
from app.infrastructure.database.dto.category_dto import CategoryDto


class CategoryReoisitory(ICategoryRepository):
    """
    カテゴリリポジトリの実装クラス

    Attributes:
        db_session: DBセッション
    """

    def __init__(self, session: Session):
        self._db_session: Session = session

    def insert(self, entity: CategoryEntity) -> CategoryEntity:
        """
        カテゴリの挿入

        Args:
            entity: 挿入するカテゴリのエンティティ
        Returns:
            CategoryEntity: 挿入したカテゴリのエンティティ
        """
        category_dto: CategoryDto = CategoryDto.from_entity(entity)
        self._db_session.add(category_dto)
        self._db_session.flush()
        self._db_session.refresh(category_dto)

        result: CategoryEntity = category_dto.to_entity()
        return result

    def find_all(self, user_id: int) -> list[CategoryEntity]:
        """
        全件取得

        Args:
            user_id: ユーザーID
        Returns:
            list[CategoryEntity]: 取得したカテゴリのエンティティのリスト
        """
        category_dto_list: list[CategoryDto] = (
            self._db_session.query(CategoryDto).filter_by(user_id=user_id).order_by(CategoryDto.id).all()
        )

        result: list[CategoryDto] = []
        for category_dto in category_dto_list:
            result.append(category_dto.to_entity())

        return result

    def find_by_id(self, id: int) -> CategoryEntity:
        """
        主キーでの取得

        Args:
            id: 主キー
        Returns:
            CategoryEntity: 取得したカテゴリのエンティティ
        """
        category_dto: CategoryDto = self._db_session.query(CategoryDto).filter_by(id=id).first()
        if not category_dto:
            return None

        result: CategoryEntity = category_dto.to_entity()
        return result

    def update(self, entity: CategoryEntity) -> CategoryEntity:
        """
        カテゴリの更新

        Args:
            entity: 更新するカテゴリのエンティティ
        Returns:
            CategoryEntity: 更新したカテゴリのエンティティ
        """
        category_dto: CategoryDto = self._db_session.query(CategoryDto).filter_by(id=entity.id).first()
        category_dto.name = entity.name
        self._db_session.flush()

        result: CategoryEntity = category_dto.to_entity()
        return result

    def delete_by_id(self, id: int) -> None:
        """
        主キーでの削除

        Args:
            id: 主キー
        """
        self._db_session.query(CategoryDto).filter_by(id=id).delete()

        return None
