import json
import os
import asyncio
import platform
from threading import Thread
from datetime import datetime

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

# Main Important Variables
SUCCESS = 0
success_last = 0
ERRORED = 0
errored_last = 0
RESET_COUNT = 0
reset_count_last = 0

client = commands.Bot(
    command_prefix=config['prefix'],
    intents=discord.Intents.all()
)
app = flask.Flask(__name__)

client.remove_command('help')


def run_web_app():
    app.run(host='0.0.0.0', port=8088)


def run_web_app_threaded():
    t = Thread(target=run_web_app)
    t.start()


@app.route("/success")
def web_success():
    global SUCCESS, success_last
    SUCCESS += 1
    success_last = SUCCESS - 1
    return f"{SUCCESS}"


@app.route("/error")
def web_error():
    global ERRORED, errored_last
    ERRORED += 1
    errored_last = ERRORED - 1
    return f"{ERRORED}"


@app.route("/reset")
def web_reset():
    global SUCCESS, ERRORED, RESET_COUNT, reset_count_last, success_last, errored_last
    RESET_COUNT += 1
    SUCCESS = 0
    ERRORED = 0
    success_last = SUCCESS
    errored_last = ERRORED
    reset_count_last = RESET_COUNT - 1
    return "Done"


@app.route("/")
def web_index():
    global SUCCESS, ERRORED, RESET_COUNT
    return flask.render_template_string(r"""<html><head> <title>API</title> <style type="text/css"> .tg { border-collapse: collapse; border-spacing: 0; } .tg td { border-color: black; border-style: solid; border-width: 1px; font-family: Arial, sans-serif; font-size: 14px; overflow: hidden; padding: 10px 5px; word-break: normal; } .tg th { border-color: black; border-style: solid; border-width: 1px; font-family: Arial, sans-serif; font-size: 14px; font-weight: normal; overflow: hidden; padding: 10px 5px; word-break: normal; } .tg .tg-0pky { border-color: inherit; text-align: left; vertical-align: top } </style></head><body> <h1 style="text-align: center;">API</h1> <table class="tg"> <thead> <tr> <th class="tg-0pky">Endpoint</th> <th class="tg-0pky">Request</th> <th class="tg-0pky">Returns</th> <th class="tg-0pky">Description</th> </tr> </thead> <tbody> <tr> <td class="tg-0pky"> <a href="/success">/success</a> </td> <td class="tg-0pky">GET</td> <td class="tg-0pky">total success count</td> <td class="tg-0pky">GET this to increment the total success count by one</td> </tr> <tr> <td class="tg-0pky"> <a href="/error">/error</a> </td> <td class="tg-0pky">GET</td> <td class="tg-0pky">total error count</td> <td class="tg-0pky">GET this to increment the total error count by one</td> </tr> <tr> <td class="tg-0pky"> <a href="/reset">/reset</a> </td> <td class="tg-0pky">GET</td> <td class="tg-0pky">None</td> <td class="tg-0pky">GET this to reset total error and success count</td> </tr> </tbody> </table> """ + r"""<h2>Success:</h2><h3>""" + str(SUCCESS) + r"""</h3><h2>Errored:</h2><h3>""" + str(ERRORED) + r"""</h3><h2>Reset Count:</h2><h3>""" + str(RESET_COUNT) + r"""</h3>""" + r"""</body></html>""")


@client.event
async def on_ready():
    global SUCCESS, ERRORED, RESET_COUNT, reset_count_last, success_last, errored_last

    print(f'Logged in as {client.user.name}')
    print(f'Discord.py API version: {discord.__version__}')
    print(f'Python version: {platform.python_version()}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"teamsds.net/discord"))
    print('Bot is ready!')

    channel = client.get_channel(config['updates_channel'])

    await channel.send(f"The bot is up and running on `{platform.platform()}` on Python `{platform.python_version()}` with Discord API version `{discord.__version__}`")

    while True:
        if not((SUCCESS == success_last) and (ERRORED == errored_last) and (RESET_COUNT == reset_count_last)):
            success_last = SUCCESS
            errored_last = ERRORED
            reset_count_last = RESET_COUNT
            await channel.send(f"**Success: ** `{SUCCESS}`\n**Error: ** `{ERRORED}`\n**Reset Count: ** `{RESET_COUNT}`\n-----")

        await asyncio.sleep(config['check_time'])


@client.command()
async def flood(ctx, to, times):
    """
    Usage:
        .flood <phone_number> <amount>

    Examples:
        .flood +94718898898 50

    Arguments:
        <phone_number>
            The phone number to flood calls for

        <amount>
            The amount of calls to flood with

    ---------------
    Developer's Notes
        ./Flood.sh +94782386009 10
        Flood this phone number: +94782386009 for 10 times
    """

    try:
        os.system(f"{config['script_name']} {times} {to}")
    except Exception as e:
        await ctx.send(f"```{e}```")
        return

    await ctx.send(f"Flooding {to} with {times} calls - Check <#{config['updates_channel']}> for updates")


@client.command()
async def reset(ctx):
    """
    Usage:
        .reset
    """

    global SUCCESS, ERRORED, RESET_COUNT, reset_count_last, success_last, errored_last

    RESET_COUNT += 1
    SUCCESS = 0
    ERRORED = 0
    success_last = SUCCESS
    errored_last = ERRORED
    reset_count_last = RESET_COUNT - 1

    await ctx.send(f"Done!")


@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(
        title="An error has occured",
        color=0xff0000,
        timestamp=datetime.utcnow()
    )
    embed.set_author(
        name=str(client.user.name),
        icon_url=str(client.user.avatar_url)
    )

    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(
            name="Error:",
            value="Missing Required Argument. Not all arguments for the usage of this command was passed. Please refer help.",
            inline=False
        )

    embed.set_footer(text=f"Reuqested by {ctx.author.name}")
    await ctx.send(embed=embed)


@client.command()
async def help(ctx, subcommand=None):

    embed = discord.Embed(
        title=f"Help for {client.user.name}",
        color=0xff0000,
        description=f"run `{config['prefix']}help [command_name]` to view additional information",
        timestamp=datetime.utcnow(),
        url="https://gifgang.net/links"
    )
    embed.set_author(
        name=str(client.user.name),
        icon_url=str(client.user.avatar_url)
    )

    if subcommand == "reset":
        embed.add_field(
            name="Usage",
            value=f"`{config['prefix']}reset`",
            inline=False
        )
        embed.add_field(
            name="Description",
            value=f"Resets the total successfull call count, total errored call count for <#{config['updates_channel']}>",
            inline=False
        )
    elif subcommand == "flood":
        embed.add_field(
            name="Usage",
            value=f"`{config['prefix']}flood <phone_number> <amount>`",
            inline=False
        )
        embed.add_field(
            name="Examples",
            value=f"`{config['prefix']}flood +94718898898 50`",
            inline=False
        )
        embed.add_field(
            name="Arguments",
            value="**<phone_number>**\n`The phone number to flood calls for`\n**<amount>**\n`The amount of calls to flood with`",
            inline=False
        )
        embed.add_field(
            name="Description",
            value=f"Flood a given phone number for the given number of times with calls",
        )
    else:
        embed.add_field(
            name="Commands",
            value=f"`{config['prefix']}help`\n`{config['prefix']}flood`\n`{config['prefix']}reset`",
            inline=False
        )

    embed.set_footer(text=f"Reuqested by {ctx.author.name}")

    await ctx.send(embed=embed)

run_web_app_threaded()
client.run(TOKEN, reconnect=True)
