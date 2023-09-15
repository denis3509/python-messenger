import logging

from aiohttp import web

from core.socketio import sio
from core import socketio_handlers

logger = logging.getLogger()

# load handlers

app = web.Application()
sio.attach(app)


async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


# app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)
