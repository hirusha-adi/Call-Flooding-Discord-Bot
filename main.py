import json
import os
import subprocess

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


client.run(TOKEN)
