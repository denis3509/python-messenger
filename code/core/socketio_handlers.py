from sqlalchemy.orm import Session

from core import db, service
from server import sio


@sio.on("user:sign_up")
@sio.base_event_handler
def sign_up(sid, data):
    print("signup ", sid)

    username = data["username"]
    password = data["password"]
    with Session(db.main_engine) as session, session.begin():
        service.User.sign_up(session, username, password)


@sio.on("user:sign_in")
@sio.base_event_handler
def sign_in(sid, data):
    username = data["username"]
    password = data["password"]
    with Session(db.main_engine) as session, session.begin():
        user = service.User.sign_in(session, username, password)
    sio.save_session(sid, user.as_dict())
    return user.as_dict()
