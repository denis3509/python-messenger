from datetime import datetime, timedelta
from typing import List

from faker import Faker
from sqlalchemy.orm import Session

from core import models as mdl


class BaseFaker(Faker):
    def __init__(self, session: Session, auto_commit=True, auto_refresh=True):
        super().__init__()
        self._session = session
        self._auto_commit = auto_commit
        self._auto_refresh = auto_refresh

    def _add(self, items: object | List[object]):
        if isinstance(items, list):
            self._session.add_all(items)
        else:
            self._session.add(items)
        self._commit()
        self._refresh(items)

    def _commit(self):
        """commit if self.autocommit is True"""
        if self._auto_commit:
            self._session.commit()

    def _refresh(self, items: object | List[object]):
        if self._auto_refresh:
            if isinstance(items, list):
                for item in items:
                    self._session.refresh(item)
            else:
                self._session.refresh(items)

    def bool(self):
        return self.random.choice([False,True])

    def timestamp(self):
        ts = datetime.utcnow()
        rand_minutes = self.random.randrange(60*24*10)
        ts = ts + self.bool() * timedelta(minutes=rand_minutes)

        return ts
    def user(self, username: str = None, password: str = None, add=True):
        """create fake user"""
        hashed_password = mdl.User.hash_password(password) if password else mdl.User.hash_password("pass")
        user = mdl.User(username="[fake]_" + self.user_name() or username,
                        hashed_password=hashed_password
                        )
        if add:
            self._add(user)
        return user

    def users(self, amount: int = 5, add=True):
        """bulk create fake users"""
        _users = []
        for i in range(amount):
            _users.append(self.user(add=False))
        if add:
            self._add(_users)
        return _users

faker = BaseFaker(None)
print(faker.timestamp())
print(faker.timestamp())
print(faker.timestamp())
print(faker.timestamp())
print(faker.timestamp())