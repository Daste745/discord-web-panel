import json
import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.discord import make_discord_blueprint, discord

with open("config.json") as f:
    config = json.load(f)

app = Flask(__name__)
app.secret_key = config["app_secret"]

# so authlib won't be shouting at us for insecure oauth2.0
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

blueprint = make_discord_blueprint(
    client_id=config["app_id"],
    client_secret=config["app_secret"]
)

app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    if not discord.authorized:
        return redirect(url_for("discord.login"))
    resp = discord.get("/api/v6/users/@me")
    user = json.loads(resp.content)
    return f"Hi there {user['username']}#{user['discriminator']}!"


if __name__ == "__main__":
    app.run(port=5000)