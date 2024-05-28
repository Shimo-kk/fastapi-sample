from app.infrastructure.database.database_handller import DatabaseHandller
from app.domain.user.user_repository import IUserRepository
from app.domain.user.user_entity import UserEntity


def test_insert_ok(injector):
    """
    挿入 OK
    """
    database_handller: DatabaseHandller = injector.get(DatabaseHandller)

    name: str = "test user"
    email: str = "test@exapmle.com"
    password: str = "testtest"

    try:
        with database_handller.begin_transaction() as repository_factory:
            user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
            new_user_entity: UserEntity = UserEntity.create(name=name, email=email, password=password)
            user_entity: UserEntity = user_repository.insert(entity=new_user_entity)

    except Exception:
        assert False

    assert user_entity.id is not None
    assert user_entity.created_at is not None
    assert user_entity.updated_at is not None
    assert user_entity.name == name
    assert user_entity.email == email
    assert user_entity.verify_password(password)


def test_not_exists_true(injector):
    """
    存在していないか確認
    """
    database_handller: DatabaseHandller = injector.get(DatabaseHandller)

    email: str = "test@exapmle.com"

    try:
        with database_handller.begin_transaction() as repository_factory:
            user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
            not_exists: bool = user_repository.not_exists(email=email)

    except Exception:
        assert False

    assert not_exists


def test_not_exists_false(injector):
    """
    存在していないか確認
    """
    database_handller: DatabaseHandller = injector.get(DatabaseHandller)

    email: str = "test1@example.com"

    try:
        with database_handller.begin_transaction() as repository_factory:
            user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
            not_exists: bool = user_repository.not_exists(email=email)

    except Exception:
        assert False

    assert not_exists is False


def test_fine_by_id_ok(injector):
    """
    主キーで取得
    """
    database_handller: DatabaseHandller = injector.get(DatabaseHandller)

    id: int = 1

    try:
        with database_handller.begin_transaction() as repository_factory:
            user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
            user_entity: UserEntity = user_repository.find_by_id(id=id)

    except Exception:
        assert False

    assert user_entity.id == id
    assert user_entity.name == "test user1"
    assert user_entity.email == "test1@example.com"
    assert user_entity.verify_password("testtest")


def test_fine_by_email_ok(injector):
    """
    主キーで取得
    """
    database_handller: DatabaseHandller = injector.get(DatabaseHandller)

    email: str = "test1@example.com"

    try:
        with database_handller.begin_transaction() as repository_factory:
            user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
            user_entity: UserEntity = user_repository.find_by_email(email=email)

    except Exception:
        assert False

    assert user_entity.id == 1
    assert user_entity.name == "test user1"
    assert user_entity.email == email
    assert user_entity.verify_password("testtest")


def test_update_ok(injector):
    """
    更新 正常
    """
    database_handller: DatabaseHandller = injector.get(DatabaseHandller)

    try:
        with database_handller.begin_transaction() as repository_factory:
            user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
            user_entity: UserEntity = user_repository.find_by_id(id=1)
            user_entity.change_name("test user updated")
            updated_user_entity: UserEntity = user_repository.update(entity=user_entity)
    except Exception:
        assert False

    assert updated_user_entity.updated_at > user_entity.updated_at
    assert updated_user_entity.name == "test user updated"
    assert updated_user_entity.email == user_entity.email
    assert updated_user_entity.password == user_entity.password


def test_delete_ok(injector):
    """
    削除 正常
    """
    database_handller: DatabaseHandller = injector.get(DatabaseHandller)

    try:
        with database_handller.begin_transaction() as repository_factory:
            user_repository: IUserRepository = repository_factory.get_repository(IUserRepository)
            user_repository.delete_by_id(id=1)
            user_entity: UserEntity = user_repository.find_by_id(id=1)

    except Exception:
        assert False

    assert user_entity is None
