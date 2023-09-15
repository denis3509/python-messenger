from sqlalchemy.orm import Session

from chat.test.utils import ChatFaker
from core.db.index import Base, main_engine
from chat import models as chat_mdl
from core import models as core_mdl


class DatabaseGenerator:
    """generates mock data for testing purposes"""
    def __init__(self, session: Session, engine):
        self._session = session
        self._engine = engine

    def drop_and_create_tables(self):
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    def users(self):
        chat_faker = ChatFaker(self._session, auto_commit=False, auto_refresh=False)
        chat_faker.users(5)

    def chat_messages(self):
        chat_faker = ChatFaker(self._session, auto_commit=False, auto_refresh=False)
        dialogs_user_ids = [(1, 2),
                            (2, 1),
                            (1, 3),
                            (3, 1),
                            (2, 3),
                            (3, 2)
                            ]
        messages = []
        for dui in dialogs_user_ids:
            u1 = self._session.get(core_mdl.User, dui[0])
            u2 = self._session.get(core_mdl.User, dui[1])
            dialog = chat_faker.dialog(u1.id, u2.id, 10, add=False)
            messages.extend(dialog)
        self._session.add_all(messages)


def recreate_db():
    with Session(main_engine) as session, session.begin():
        db_gen = DatabaseGenerator(session, main_engine)
        db_gen.drop_and_create_tables()
        db_gen.users()
        db_gen.chat_messages()


def main():
    recreate_db()


if __name__ == "__main__":
    main()
