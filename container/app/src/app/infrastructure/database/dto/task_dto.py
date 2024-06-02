from sqlalchemy import Column, INTEGER, VARCHAR, TEXT, DATE, BOOLEAN, ForeignKey
from app.infrastructure.database.dto import BaseDto
from app.domain.task.task_entity import TaskEntity


class TaskDto(BaseDto):
    """
    カテゴリのDTOクラス

    Attributes:
        user_id: ユーザーID
        title: タイトル
        detail: 詳細
        priority_id: 優先度
        category_id: カテゴリ
        start_date: 開始日
        is_done: 完了したか
    """

    __tablename__ = "tasks"

    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="ユーザーID")
    title = Column(VARCHAR(50), nullable=False, comment="タイトル")
    detail = Column(TEXT, nullable=True, comment="詳細")
    priority_id = Column(INTEGER, nullable=False, comment="優先度ID")
    category_id = Column(INTEGER, nullable=False, comment="カテゴリID")
    start_date = Column(DATE, nullable=True, comment="開始日")
    is_done = Column(BOOLEAN, nullable=False, default=False, comment="完了フラグ")

    @staticmethod
    def from_entity(entity: TaskEntity) -> "TaskDto":
        return TaskDto(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            user_id=entity.user_id,
            title=entity.title,
            detail=entity.detail,
            priority_id=entity.priority_id,
            category_id=entity.category_id,
            start_date=entity.start_date,
            is_done=entity.is_done,
        )

    def to_entity(self) -> TaskEntity:
        return TaskEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            title=self.title,
            detail=self.detail,
            priority_id=self.priority_id,
            category_id=self.category_id,
            start_date=self.start_date,
            is_done=self.is_done,
        )
