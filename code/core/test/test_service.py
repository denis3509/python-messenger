from unittest import TestCase

import pytest as pytest
from sqlalchemy import create_engine, URL, select
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from core import models as mdl, config, service, db


#
# @pytest.fixture()
# def db_session(setup_database, connection):
#
#     transaction = connection.begin()
#     yield scoped_session(
#         sessionmaker(autocommit=False, autoflush=False, bind=connection)
#     )
#     transaction.rollback()


def test_sign_up(db_session):
    # sign up
    username = "[username]"
    password = "[password]"
    service.User.sign_up(db_session, username, password)
    stmt = select(mdl.User).where(mdl.User.username == username)
    user = db_session.scalars(stmt).one()

    assert user.id is not None
    assert user.username == username

    db_session.commit()

    service.User.sign_in(db_session, username, password)
