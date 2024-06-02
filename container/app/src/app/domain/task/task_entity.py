from datetime import datetime, date
from app.core.exceptions import ValidationError
from app.domain import BaseEntity
from app.domain.task.task_validator import TaskValidator


class TaskEntity(BaseEntity):
    """
    カテゴリのエンティティクラス

    Attributes:
        user_id: ユーザーID
        title: タイトル
        detail: 詳細
        priority_id: 優先度
        category_id: カテゴリ
        start_date: 開始日
        is_done: 完了したか
    """

    @staticmethod
    def create(
        user_id: int,
        title: str,
        detail: str,
        priority_id: int,
        category_id: int,
        start_date: date,
    ) -> "TaskEntity":
        """
        エンティティの作成

        Args:
            user_id: ユーザーID
            title: タイトル
            detail: 詳細
            priority_id: 優先度
            category_id: カテゴリ
            start_date: 開始日
            is_done: 完了したか
        """

        # タイトルのバリデーション
        valid_message: str = TaskValidator.validate_title(value=title)
        if valid_message:
            raise ValidationError(valid_message)

        # 開始日のバリデーション
        valid_message: str = TaskValidator.validate_start_date(value=start_date)
        if valid_message:
            raise ValidationError(valid_message)

        return TaskEntity(
            user_id=user_id,
            title=title,
            detail=detail,
            priority_id=priority_id,
            category_id=category_id,
            start_date=start_date,
            is_done=False,
        )

    def __init__(
        self,
        id: int = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        user_id: int = 0,
        title: str = "",
        detail: str = "",
        priority_id: int = 0,
        category_id: int = 0,
        start_date: date = None,
        is_done: bool = False,
    ):
        """
        Args:
            id: 主キー
            created_at: 作成日時
            updated_at: 更新日時
            user_id: ユーザーID
            title: タイトル
            detail: 詳細
            priority_id: 優先度
            category_id: カテゴリ
            start_date: 開始日
            is_done: 完了したか
        """
        BaseEntity.__init__(self, id, created_at, updated_at)
        self._user_id: int = user_id
        self._title: str = title
        self._detail: str = detail
        self._priority_id: int = priority_id
        self._category_id: int = category_id
        self._start_date: date = start_date
        self._is_done: bool = is_done

    def __eq__(self, o: object) -> bool:
        """
        Args:
            o: オブジェクト
        """
        return BaseEntity.__eq__(o)

    def change_title(self, title: str):
        """
        タイトルの変更

        Args:
            title: タイトル
        """

        # タイトルのバリデーション
        valid_message: str = TaskValidator.validate_title(value=title)
        if valid_message:
            raise ValidationError(valid_message)

        self._title = title

    def change_detail(self, detail: str):
        """
        詳細の変更

        Args:
            detail: 詳細
        """

        self._detail = detail

    def change_priority_id(self, priority_id: int):
        """
        優先度の変更

        Args:
            priority_id: 優先度ID
        """

        self._priority_id = priority_id

    def change_category_id(self, category_id: int):
        """
        カテゴリの変更

        Args:
            category_id: カテゴリID
        """

        self._category_id = category_id

    def change_start_date(self, start_date: int):
        """
        開始日の変更

        Args:
            start_date: 開始日
        """

        self._start_date = start_date

    def done(self):
        """
        タスクの完了
        """
        self._is_done = True

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def detail(self) -> str:
        return self._detail

    @property
    def priority_id(self) -> int:
        return self._priority_id

    @property
    def category_id(self) -> int:
        return self._category_id

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def is_done(self) -> bool:
        return self._is_done
