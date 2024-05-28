from injector import Module, provider, singleton
from app.application.interface.database.database_handller import IDatabaseHandller
from app.application.interface.usecase.auth_usecase import IAuthUsecase
from app.infrastructure.database.database_handller import (
    DatabaseHost,
    DatabaseUser,
    DatabasePass,
    DatabaseName,
    DatabaseHandller,
)
from app.application.usecase.auth_usecase import AuthUsecase


class DependencyModule(Module):
    """
    依存関係設定モジュール
    """

    def __init__(self, db_host: str, db_user: str, db_pass: str, db_name: str):
        self._db_host = db_host
        self._db_user = db_user
        self._db_pass = db_pass
        self._db_name = db_name

    def configure(self, binder):
        binder.bind(IDatabaseHandller, to=DatabaseHandller, scope=singleton)
        binder.bind(IAuthUsecase, to=AuthUsecase, scope=singleton)

    @singleton
    @provider
    def database_host(self) -> DatabaseHost:
        return self._db_host

    @singleton
    @provider
    def database_user(self) -> DatabaseUser:
        return self._db_user

    @singleton
    @provider
    def database_pass(self) -> DatabasePass:
        return self._db_pass

    @singleton
    @provider
    def database_name(self) -> DatabaseName:
        return self._db_name
