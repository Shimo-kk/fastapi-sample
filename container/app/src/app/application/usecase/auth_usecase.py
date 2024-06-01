from injector import inject, singleton
from app.application.model.auth_model import SignUpModel, SignInModel
from app.application.interface.usecase.auth_usecase import IAuthUsecase
from app.application.interface.database.database_handller import IDatabaseHandller
from app.domain.user.user_repository import IUserRepository
from app.domain.user.user_entity import UserEntity
from app.core import exceptions


@singleton
class AuthUsecase(IAuthUsecase):
    """
    認証ユースケースの実装クラス

    Attributes:
        database_handller: データベースハンドラー
    """

    @inject
    def __init__(self, database_handller: IDatabaseHandller):
        self._database_handller = database_handller

    def sign_up(self, data: SignUpModel) -> None:
        """
        サインアップ

        Args:
            data: サインアップモデル
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)

                # 同じE-mailアドレスのユーザーが存在していないか確認
                if not user_repository.not_exists(email=data.email):
                    raise exceptions.AlreadyExistsError("入力されたE-mailアドレスが既に存在しています。")

                # ユーザーのエンティティを作成
                new_user_entity: UserEntity = UserEntity.create(
                    name=data.name, email=data.email, password=data.password
                )

                # ユーザーを挿入
                user_repository.insert(entity=new_user_entity)

        except Exception:
            raise

    def sign_in(self, data: SignInModel) -> str:
        """
        サインイン

        Args:
            data: サインインモデル
        """
        try:
            with self._database_handller.begin_transaction() as repository_factory:
                user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)

                # E-mailでユーザーを取得
                user_entity: UserEntity = user_repository.find_by_email(email=data.email)

                # ユーザーが存在しない場合は例外を投げる
                if not user_entity:
                    raise exceptions.NotFoundError("ユーザーが存在しません。")

                # パスワードの正しくない場合は例外を投げる
                if not user_entity.verify_password(plain_pw=data.password):
                    raise exceptions.BadRequestError("パスワードが一致しません。")

                return user_entity.email

        except Exception:
            raise
