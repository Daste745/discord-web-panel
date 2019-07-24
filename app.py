import asyncio
from typing import Iterator, Coroutine
from collections import defaultdict
import threading

import aiohttp

from sanic import Sanic
from sanic.request import Request
from sanic.response import text, json, HTTPResponse
from sanic_oauth.blueprint import oauth_blueprint, login_required
from sanic_oauth.providers import DiscordClient
from sanic_jinja2 import SanicJinja2

from discord_entites import User, Guild, get_user, get_guilds
from setup_sanic import get_config, get_app, Config

import discord
from discord.ext.commands import Bot

config: Config = get_config()
app: Sanic = get_app(__name__)
jinja: SanicJinja2 = SanicJinja2(app)
bot: Bot = Bot(command_prefix="!wp ")


@bot.command(name="owo")
async def owo(ctx: discord.ext.commands.Context) -> None:
    await ctx.send("uwu")


@app.route("/")
@login_required(add_user_info=False)
async def index(request: Request) -> HTTPResponse:
    provider: DiscordClient = request.app.oauth_factory(**{'access_token': request['session']['token']})
    user: User = await get_user(provider)
    guilds: Iterator[Guild] = await get_guilds(provider)
    return jinja.render("index.html", request, user=user, guilds=guilds)


if __name__ == "__main__":
    sanic_thread: threading.Thread = threading.Thread(target=app.run, kwargs={"port": 5000})

    def run_bot() -> None:
        bot.run(config.bot_token)
    bot_thread: threading.Thread = threading.Thread(target=run_bot)
    sanic_thread.start()
    bot_thread.start()
