import logging

import socketio

logger = logging.getLogger()


class AsyncServer(socketio.AsyncServer):
    def auth_only(self, fn):
        def wrapped(sid, data):
            if self.get_session(sid) is not None:
                return None, fn(sid, data)
            else:
                return "Permission Denied", None

        return wrapped

    @staticmethod
    def base_event_handler(fn):
        def wrapped(sid, data):
            try:
                print(fn.__name__)
                result = fn(sid, data)
                return None, result
            except BaseException as e:
                logger.error(e)
                return str(e), None

        return wrapped


sio = AsyncServer()
