import pytest
from sqlalchemy import select
from chat.test.utils import ChatFaker
from core import models as core_mdl
from chat import service, models as mdl
from conftest import users


@pytest.mark.parametrize("sender_id,recipient_id,error",
                         [
                             (1, 1, ValueError),
                             (0, 1, PermissionError),
                             (1, 2, None)
                         ])
def test_create_message(sender_id, recipient_id, error,
                        db_session, faker):
    user1 = db_session.get(core_mdl.User, sender_id)
    # user2 = db_session.get(core_mdl.User, recipient_id)
    message = service.CreateMessageDTO.match_kwargs(recipient_id=recipient_id,
                                                    text="text")
    if error:
        with pytest.raises(error):
            chat_service = service.Chat(db_session, user1)
            chat_service.create_message(message)
    else:
        chat_service = service.Chat(db_session, user1)
        message = chat_service.create_message(message)
        assert message in db_session.new


def test_read_dialog(db_session):
    user1 = db_session.get(core_mdl.User, 1)
    user2 = db_session.get(core_mdl.User, 2)
    faker = ChatFaker(db_session)
    faker.dialog(user1.id, user2.id, amount=5)

    chat_service = service.Chat(db_session, user2)
    chat_service.read_contact_messages(user1.id)

    stmt = (select(mdl.ChatMessage)
            .where(mdl.ChatMessage.sender_id == user1.id
                   and mdl.ChatMessage.recipient_id == user2.id)
            )
    dialog = db_session.scalars(stmt).all()
    for message in dialog:
        assert message.read == True


def test_contact_list(db_session):
    user1 = db_session.get(core_mdl.User, 1)
    user2 = db_session.get(core_mdl.User, 2)
    user3 = db_session.get(core_mdl.User, 3)
    faker = ChatFaker(db_session)
    faker.dialog(user1.id, user2.id, amount=5)
    faker.dialog(user1.id, user3.id, amount=5)

    chat_service = service.Chat(db_session, user1)
    contact_list = chat_service.contact_list()
    assert len(contact_list) == 2
