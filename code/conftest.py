import pytest as pytest
from faker import Faker
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session

from core import models as mdl
from core.config import SETTINGS

# https://itnext.io/setting-up-transactional-tests-with-pytest-and-sqlalchemy-b2d726347629
@pytest.fixture(scope="session")
def connection():
    print("connection")

    test_engine = create_engine(URL.create(**SETTINGS.test_db_dict()))
    return test_engine.connect()


@pytest.fixture(scope="session")
def test_engine():
    print("test_engine")
    test_engine = create_engine(URL.create(**SETTINGS.test_db_dict()))
    return test_engine


def seed_database(session):
    users(session)


@pytest.fixture(scope="session")
def setup_database(test_engine):
    print("setup database")
    mdl.Base.metadata.drop_all(test_engine)
    mdl.Base.metadata.create_all(test_engine)
    with Session(test_engine) as session, session.begin():
        seed_database(session)
    yield

    mdl.Base.metadata.drop_all(test_engine)


#
# @pytest.fixture(scope="session")
# def setup_database(connection):
#     print("setup database")
#     mdl.Base.metadata.drop_all(connection)
#     mdl.Base.metadata.create_all(connection)
#     users()
#     connection.commit()
#     yield
#
#     mdl.Base.metadata.drop_all(connection)
#

@pytest.fixture()
def db_session(setup_database, test_engine):
    session = Session(test_engine)

    session.begin(nested=True)

    yield session
    session.rollback()
    session.close()


def users(session):
    print("users call")
    _users = [
        mdl.User(
            username="user1",
            hashed_password="pass"
        ),
        mdl.User(
            username="user2",
            hashed_password="pass"
        ),
        mdl.User(
            username="user3",
            hashed_password="pass"
        ),
    ]

    session.add_all(_users)

    return users

