from unittest import mock
from unittest.mock import MagicMock, call, ANY

from core import socketio_handlers
from core import service
from core import models as mdl
from server import sio


def test_sign_up(monkeypatch):
    # def sign_up():
    #     pass
    sign_up = MagicMock()
    monkeypatch.setattr(service.User, 'sign_up', sign_up)
    data = {
        'username': "[username]",
        'password': "[password]"
    }

    result = socketio_handlers.sign_up(1123, data)
    sign_up.assert_called_with(ANY, data["username"], data["password"])
    assert result == (None, None)

    sign_up = MagicMock()
    monkeypatch.setattr(service.User, 'sign_up', sign_up)
    sign_up.side_effect = Exception("oops")
    result2 = socketio_handlers.sign_up(1123, data)
    assert result2 == (str(Exception("oops")), None)


def test_sign_in(monkeypatch):
    # def sign_up():
    #     pass
    sign_in = MagicMock()
    user = mock.create_autospec(mdl.User)
    sign_in.return_value = user
    monkeypatch.setattr(service.User, 'sign_in', sign_in)
    save_session = MagicMock()
    monkeypatch.setattr(sio, 'save_session', save_session)
    data = {
        'username': "[username]",
        'password': "[password]"
    }
    sid = 1123

    result = socketio_handlers.sign_in(sid, data)
    sign_in.assert_called_with(ANY, data["username"], data["password"])
    save_session.assert_called_with(sid, user.as_dict())
    assert result == (None, user.as_dict())


