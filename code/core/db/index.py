import sys
from datetime import datetime

import sqlalchemy
from sqlalchemy import create_engine, URL, func, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.ddl import CreateTable

from core.config import SETTINGS

main_engine = create_engine(URL.create(**SETTINGS.db_dict()), echo=True)
print(URL.create(**SETTINGS.db_dict()))


def create_session():
    return Session(main_engine)


def print_ddls(model):
    for t in model.metadata.tables.values():
        print(CreateTable(t).compile(main_engine))


def check_db():
    with Session(main_engine) as session, session.begin():
        try:
            session.execute(text("select now();"))
        except sqlalchemy.exc.OperationalError as e:
            print("Database connection failed", file=sys.stderr)
            print(e, file=sys.stderr)

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())
