from concurrent.futures import Executor
from typing import Iterator
import concurrent.futures

from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic_oauth.blueprint import login_required
from sanic_oauth.providers import DiscordClient
from sanic_jinja2 import SanicJinja2

from discord_web_panel.discord_entites import User, Guild, get_user, get_guilds
from discord_web_panel.setup_sanic import get_config, get_app, Config

import discord
from discord.ext.commands import Bot

config: Config = get_config()
app: Sanic = get_app("discord_web_panel")
jinja: SanicJinja2 = SanicJinja2(app)
bot: Bot = Bot(command_prefix="!wp ")


@bot.command(name="ping")
async def owo(ctx: discord.ext.commands.Context) -> None:
    await ctx.send("pong")


@app.route("/")
@login_required(add_user_info=False)
async def index(request: Request) -> HTTPResponse:
    provider: DiscordClient = request.app.oauth_factory(**{'access_token': request['session']['token']})
    user: User = await get_user(provider)
    guilds: Iterator[Guild] = await get_guilds(provider)
    return jinja.render("index.html", request, user=user, guilds=guilds)


def run_bot() -> None:
    bot.run(config.bot_token)


def run_sanic() -> None:
    app.run(port=5000, register_sys_signals=False)


if __name__ == "__main__":
    executor: Executor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(run_bot)
        executor.submit(run_sanic)


