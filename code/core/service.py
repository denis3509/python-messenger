from sqlalchemy import select
from sqlalchemy.orm import Session
from core import models as mdl

import bcrypt

from core.db import main_engine
from core import db
from core.exceptions import AuthError


class User:
    @staticmethod
    def sign_up(session, username: str, password: str):
        hashed = mdl.User.hash_password(password)
        user = mdl.User(username=username, hashed_password=hashed)
        session.add(user)


    @staticmethod
    def sign_in(session, username: str, password: str) -> mdl.User:
        stmt = select(mdl.User).where(mdl.User.username == username)
        user = session.scalars(stmt).one()

        if not user.is_valid_pass(password):
            raise AuthError("wrong username or password")
        return user

