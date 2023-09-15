import re
from datetime import datetime
from typing import List

import bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, relationship, Session, validates
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.ddl import CreateTable

from core.db.index import Base, main_engine


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(1000))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r})"

    def is_valid_pass(self, password):
        is_valid = bcrypt.checkpw(password.encode("utf-8"), self.hashed_password.encode("utf-8"))
        return is_valid

    @staticmethod
    def by_username(session, username):
        pass

    @staticmethod
    def hash_password(password):
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    def as_dict(self):
        as_dict = {
            'username': self.username
        }
        return as_dict

    @validates("username")
    def validates_username(self, key, username: str):
        re_match = re.match(r"^[A-Za-z\[\]][\[\]A-Za-z0-9_.]{3,29}$", username)
        if re_match is None:
            raise ValueError(f"Username '{username}' is invalid")
        return username
