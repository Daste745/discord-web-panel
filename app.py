from json import load as load_json
import aiohttp
import aiohttp.web_exceptions
from sanic import Sanic
from sanic.request import Request
from sanic.response import text, json, HTTPResponse
from sanic_oauth.blueprint import oauth_blueprint, login_required
from sanic_session import InMemorySessionInterface
from discord_entites import User, Guild, get_user, get_guilds

with open("config.json") as f:
    config = load_json(f)

app = Sanic(__name__)
app.blueprint(oauth_blueprint)
app.session_interface = InMemorySessionInterface()
app.config.OAUTH_PROVIDER = "sanic_oauth.providers.DiscordClient"
app.config.OAUTH_REDIRECT_URI = "http://127.0.0.1:5000/oauth"
app.config.OAUTH_SCOPE = 'identify guilds'
app.config.OAUTH_CLIENT_ID = config["app_id"]
app.config.OAUTH_CLIENT_SECRET = config["app_secret"]
# TODO: get a module and push above to a function


@app.listener("before_server_start")
async def init_aiohttp_session(sanic_app, _loop):
    sanic_app.async_session = aiohttp.ClientSession()


@app.listener("after_server_stop")
async def close_aiohttp_session(sanic_app, _loop):
    await sanic_app.async_session.close()


@app.middleware("request")
async def add_session_to_request(request: Request):
    await request.app.session_interface.open(request)


@app.middleware("response")
async def save_session(request: Request, response: HTTPResponse):
    await request.app.session_interface.save(request, response)


@app.route("/")
@login_required(add_user_info=False)
async def index(request: Request) -> HTTPResponse:
    provider = request.app.oauth_factory(**{'access_token': request['session']['token']})
    user = await get_user(provider)
    guilds = await get_guilds(provider)
    return text(f"uwu hi there {user.username}#{user.discriminator}!"
                f"\ni was uwu waiting for you uwu \nyou're in {len(list(guilds))} guilds!")

if __name__ == "__main__":
    app.run(port=5000)
    print("owo")
