from typing import Type, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.infrastructure.database.dto.priority_dto import PriorityDto

T = TypeVar("T")


def seed(url: str) -> None:
    engine = create_engine(url)
    session_local: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()

    try:
        # 優先度
        priorities: list[PriorityDto] = [
            PriorityDto(id=1, name="高"),
            PriorityDto(id=2, name="中"),
            PriorityDto(id=3, name="低"),
        ]
        _seed(session=session, cls=PriorityDto, data_list=priorities)

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _seed(session: Session, cls: Type[T], data_list: list[T]):
    print("Seed:" + str(cls))

    # 既存のデータを取得
    existing_data = session.query(cls).all()
    existing_data_dict = {record.id: record for record in existing_data}
    data_list_dict = {record.id: record for record in data_list}

    # 挿入またはスキップするレコードを処理
    for record in data_list:
        if record.id in existing_data_dict:
            existing_record = existing_data_dict[record.id]
            # 既存のレコードと内容が同じ場合はスキップ
            if all(
                getattr(existing_record, attr) == getattr(record, attr)
                for attr in vars(record)
                if not attr.startswith("_")
            ):
                continue
            # 既存のレコードと内容が異なる場合はスキップ
            else:
                continue
        else:
            # 新しいレコードを追加
            session.add(record)

    # data_listに存在しない既存レコードを削除
    for record in existing_data:
        if record.id not in data_list_dict:
            session.delete(record)
