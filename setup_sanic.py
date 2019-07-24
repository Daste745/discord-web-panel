from collections import defaultdict

import aiohttp
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic_oauth.blueprint import oauth_blueprint
from sanic_session import InMemorySessionInterface

from config import get_config, Config


def get_app(name) -> Sanic:
    config: Config = get_config()
    app: Sanic = Sanic(name)
    app.blueprint(oauth_blueprint)
    app.session_interface = InMemorySessionInterface()

    app.config.OAUTH_REDIRECT_URI = "http://127.0.0.1:5000/oauth"
    app.config.OAUTH_PROVIDER = 'sanic_oauth.providers.DiscordClient'
    app.config.OAUTH_SCOPE = "identify guilds"
    app.config.OAUTH_CLIENT_ID = config.app_id
    app.config.OAUTH_CLIENT_SECRET = config.app_secret

    async def init_aiohttp_session(sanic_app: Sanic, _loop) -> None:
        sanic_app.async_session = aiohttp.ClientSession()

    async def close_aiohttp_session(sanic_app: Sanic, _loop) -> None:
        await sanic_app.async_session.close()

    async def add_session_to_request(request: Request) -> None:
        await request.app.session_interface.open(request)

    async def save_session(request: Request, response: HTTPResponse) -> None:
        await request.app.session_interface.save(request, response)

    app.listener("before_server_start")(init_aiohttp_session)
    app.listener("after_server_stop")(close_aiohttp_session)
    app.middleware("request")(add_session_to_request)
    app.middleware("response")(save_session)
    return app
