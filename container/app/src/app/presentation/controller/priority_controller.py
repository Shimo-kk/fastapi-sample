from injector import inject, singleton
from app.application.model.priority_model import PriorityReadModel
from app.application.interface.usecase.priority_usecase import IPriorityUsecase


@singleton
class PriorityController:
    """
    優先度コントローラークラス
    """

    @inject
    def __init__(self, priority_usecase: IPriorityUsecase):
        self._priority_usecase = priority_usecase

    def get_all_priority(self) -> list[PriorityReadModel]:
        """
        全ての優先度を取得

        Returns:
            list[PriorityReadModel]: 優先度参照モデルリスト
        """

        try:
            # ユースケース実行
            return self._priority_usecase.get_all_priority()

        except Exception:
            raise
