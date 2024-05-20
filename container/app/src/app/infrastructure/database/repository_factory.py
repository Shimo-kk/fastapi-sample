from sqlalchemy.orm.session import Session

from app.application.interface.database.repository_factory import IRepositoryFactory


class RepositoryFactory(IRepositoryFactory):
    """
    リポジトリファクトリの実装クラス

    Attributes:
        session: セッション
    """

    def __init__(self, session: Session):
        self.session: Session = session
