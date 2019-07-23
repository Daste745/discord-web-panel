import json
import os
from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.discord import make_discord_blueprint, discord
from discord_entites import User, Guild
from typing import List

with open("config.json") as f:
    config = json.load(f)

app = Flask(__name__)
app.secret_key = config["app_secret"]

# so authlib won't be shouting at us for insecure oauth2.0
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

blueprint = make_discord_blueprint(
    client_id=config["app_id"],
    client_secret=config["app_secret"],
    scope=["identify", "guilds"]
)

app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    if not discord.authorized:
        return redirect(url_for("discord.login"))
    user_resp = discord.get("/api/v6/users/@me")
    user = User.from_dict(json.loads(user_resp.content))
    guilds_resp = discord.get("/api/v6/users/@me/guilds")
    guilds = map(Guild.from_dict, json.loads(guilds_resp.content))
    return render_template("index.html", user=user, guilds=guilds)


if __name__ == "__main__":
    app.run(port=5000)