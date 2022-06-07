import json
import os
import subprocess
import platform
from threading import Thread

import discord
import flask
from discord.ext import commands


# File Names
_cwd = os.getcwd()
config_filename = os.path.join(_cwd, "config.json")
token_filename = os.path.join(_cwd, "token.txt")

with open(config_filename, "r", encoding="utf-8") as _config_file:
    config = json.load(_config_file)

with open(token_filename, "r", encoding="utf-8") as _token_file:
    TOKEN = _token_file.read()


client = commands.Bot(command_prefix=config['prefix'])
app = flask.Flask(__name__)


def run_web_app():
    app.run(host='0.0.0.0', port=8090)


def run_web_app_threaded():
    t = Thread(target=run_web_app)
    t.start()


@app.route("/")
def web_index():
    return "Hello World"


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    print(f'Discord.py API version: {discord.__version__}')
    print(f'Python version: {platform.python_version()}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"teamsds.net/discord"))
    print('Bot is ready!')

run_web_app_threaded()
client.run(TOKEN)
