from datetime import datetime

from sqlalchemy import create_engine, URL, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.ddl import CreateTable

from core import config

main_engine = create_engine(URL.create(**config.DATABASE), echo=True)


def create_session():
    return Session(main_engine)


def print_ddls(model):
    for t in model.metadata.tables.values():
        print(CreateTable(t).compile(main_engine))


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())
