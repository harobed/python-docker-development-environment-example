import pathlib
import asyncio

from aiohttp import web
import jinja2
import aiohttp_jinja2

from . import views
from . import db

here = pathlib.Path(__file__).parent


def get_app(loop=None):
    app = web.Application(loop=loop)

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(here / 'templates'))
    )

    app.on_startup.append(db.init_pg)
    app.on_cleanup.append(db.close_pg)

    app.router.add_get('/', views.index)
    app.router.add_get('/poll/{question_id}', views.get_poll, name='get_poll')
    app.router.add_post('/poll/{question_id}', views.post_poll, name='post_poll')
    app.router.add_get('/poll/{question_id}/results', views.poll_results, name='poll_results')
    app.router.add_static('/static/', path=here / 'static', name='static')

    return app

def run_app(host, port):
    loop = asyncio.get_event_loop()
    app = get_app(loop)
    web.run_app(app, host=host, port=port)
