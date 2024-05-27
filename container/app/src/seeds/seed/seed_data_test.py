from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.domain.user.user_entity import UserEntity
from app.infrastructure.database.dto.user_dto import UserDto


def seed(url: str) -> None:
    engine = create_engine(url)
    session_local: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()
    try:
        seed_user(session=session)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def seed_user(session: Session) -> None:
    users: list[UserDto] = [
        UserDto.from_entity(UserEntity.create(name="test user1", email="test1@example.com", password="testtest")),
        UserDto.from_entity(UserEntity.create(name="test user2", email="test2@example.com", password="testtest")),
        UserDto.from_entity(UserEntity.create(name="test user3", email="test3@example.com", password="testtest")),
    ]
    session.add_all(users)
    session.flush()
