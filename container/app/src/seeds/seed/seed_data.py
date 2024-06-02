from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.infrastructure.database.dto.priority_dto import PriorityDto


def seed(url: str) -> None:
    engine = create_engine(url)
    session_local: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()
    try:
        seed_priority(session=session)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def seed_priority(session: Session) -> None:
    priorities: list[PriorityDto] = [
        PriorityDto(id=1, name="高"),
        PriorityDto(id=2, name="中"),
        PriorityDto(id=3, name="低"),
    ]

    for priority in priorities:
        existing_priority = session.query(PriorityDto).filter_by(id=priority.id).one_or_none()

        if existing_priority is not None:
            if existing_priority.name != priority.name:
                existing_priority.name = priority.name
        else:
            session.add(priority)

    session.flush()
