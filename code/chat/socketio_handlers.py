from sqlalchemy.orm import Session

from chat import service
from core.db import main_engine
from core.socketio import sio


@sio.on("create-message")
@sio.auth_only
@sio.base_event_handler
def create_message(sid, data):
    user = sio.get_session(sid)
    message_dto = service.CreateMessageDTO.match_kwargs(**data)
    with Session(main_engine) as session:
        chat_service = service.Chat(session, user)
        message = chat_service.create_message(message_dto)
        session.commit()
        session.refresh(message)
        return {'message_id': message.id}


@sio.on("edit-message")
@sio.auth_only
@sio.base_event_handler
def edit_message(sid, data):
    user = sio.get_session(sid)
    message_dto = service.EditMessageDTO.match_kwargs(**data)
    with Session(main_engine) as session:
        chat_service = service.Chat(session, user)
        message = chat_service.edit_message(message_dto)
        session.commit()
        session.refresh(message)
        return {'message_id': message.id}


@sio.on("delete-message")
@sio.auth_only
@sio.base_event_handler
def delete_message(sid, data):
    user = sio.get_session(sid)
    message_id = data["message_id"]
    with Session(main_engine) as session:
        chat_service = service.Chat(session, user)
        chat_service.delete_message(message_id)
        session.commit()
    return None


@sio.on("read-contact-messages")
@sio.auth_only
@sio.base_event_handler
def read_contact_messages(sid, data):
    user = sio.get_session(sid)
    contact_id = data["contact_id"]
    with Session(main_engine) as session:
        chat_service = service.Chat(session, user)
        chat_service.read_contact_messages(contact_id)
        session.commit()
    return None


@sio.on("contact-list")
@sio.auth_only
@sio.base_event_handler
def contact_list(sid, data):
    user = sio.get_session(sid)
    with Session(main_engine) as session:
        chat_service = service.Chat(session, user)
        _contact_list = chat_service.contact_list()
    result = [contact.as_dict() for contact in _contact_list]
    return {'contact_list': result}
