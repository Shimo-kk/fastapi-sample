from sqlalchemy.orm.session import Session
from app.domain.task.task_entity import TaskEntity
from app.domain.task.task_repository import ITaskRepository
from app.infrastructure.database.dto.task_dto import TaskDto


class TaskRepository(ITaskRepository):
    """
    タスクリポジトリの実装クラス

    Attributes:
        db_session: DBセッション
    """

    def __init__(self, session: Session):
        self._db_session: Session = session

    def insert(self, entity: TaskEntity) -> TaskEntity:
        """
        タスクの挿入

        Args:
            entity: 挿入するタスクのエンティティ
        Returns:
            TaskEntity: 挿入したタスクのエンティティ
        """
        task_dto: TaskDto = TaskDto.from_entity(entity)
        self._db_session.add(task_dto)
        self._db_session.flush()
        self._db_session.refresh(task_dto)

        result: TaskEntity = task_dto.to_entity()
        return result

    def find_all(self, user_id: int) -> list[TaskEntity]:
        """
        全件取得

        Args:
            user_id: ユーザーID
        Returns:
            list[TaskEntity]: 取得したタスクのエンティティのリスト
        """
        task_dto_list: list[TaskDto] = (
            self._db_session.query(TaskDto).filter_by(user_id=user_id).order_by(TaskDto.id).all()
        )

        result: list[TaskEntity] = []
        for task_dto in task_dto_list:
            result.append(task_dto.to_entity())

        return result

    def find_by_id(self, id: int) -> TaskEntity:
        """
        主キーでの取得

        Args:
            id: 主キー
        Returns:
            TaskEntity: 取得したタスクのエンティティ
        """
        task_dto: TaskDto = self._db_session.query(TaskDto).filter_by(id=id).first()
        if not task_dto:
            return None

        result: TaskEntity = task_dto.to_entity()
        return result

    def update(self, entity: TaskEntity) -> TaskEntity:
        """
        タスクの更新

        Args:
            entity: 更新するタスクのエンティティ
        Returns:
            TaskEntity: 更新したタスクのエンティティ
        """
        task_dto: TaskDto = self._db_session.query(TaskDto).filter_by(id=entity.id).first()
        task_dto.title = entity.title
        task_dto.detail = entity.detail
        task_dto.priority_id = entity.priority_id
        task_dto.category_id = entity.category_id
        task_dto.start_date = entity.start_date
        task_dto.is_done = entity.is_done
        self._db_session.flush()

        result: TaskEntity = task_dto.to_entity()
        return result

    def delete_by_id(self, id: int) -> None:
        """
        主キーでの削除

        Args:
            id: 主キー
        """
        self._db_session.query(TaskDto).filter_by(id=id).delete()

        return None
