from injector import Module, provider, singleton
from app.core.environment import DB_HOST, DB_USER, DB_PASS, DB_NAME
from app.application.interface.database.database_handller import IDatabaseHandller
from app.infrastructure.database.database_handller import (
    DatabaseHost,
    DatabaseUser,
    DatabasePass,
    DatabaseName,
    DatabaseHandller,
)


class DependencyModule(Module):
    """
    依存関係設定モジュール
    """

    def configure(self, binder):
        binder.bind(IDatabaseHandller, to=DatabaseHandller, scope=singleton)

    @singleton
    @provider
    def database_host(self) -> DatabaseHost:
        return DB_HOST

    @singleton
    @provider
    def database_user(self) -> DatabaseUser:
        return DB_USER

    @singleton
    @provider
    def database_pass(self) -> DatabasePass:
        return DB_PASS

    @singleton
    @provider
    def database_name(self) -> DatabaseName:
        return DB_NAME
