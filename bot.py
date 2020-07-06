# rice_pudding
# by brussels_sprout

# Note: You need to assign your Discord bot token
# to a Config Var named "TOKEN".

import sys
import os

# import discord
from discord.ext import commands
import logging
import random
from googletrans import Translator


# logs warnings and higher levels to console
logging.basicConfig(level=logging.WARNING)


def handle_token():
    global TOKEN
    TOKEN = os.environ["TOKEN"]


TOKEN = None
handle_token()

bot = commands.Bot(command_prefix="!h ")


@bot.event
async def on_ready():
    latency = round(bot.latency, 3) * 1000  # in ms to 3 d.p.

    print(f"Connected successfully as {bot.user} ({latency}ms).")


@bot.event
async def on_guild_join(guild):  # guild is server
    prefix = bot.command_prefix

    await guild.system_channel.send(
        f"**Hello *{guild.name}*!**\n"
        f"Prefix: \"{prefix}\" (example: *{prefix}help*)"
    )


@bot.event
async def on_message(message):
    if message.author != bot.user:
        if "pog" in message.content.lower():
            await message.channel.send("Poggers!")

    if str(bot.user.id) in message.content:
        await message.channel.send("Huh?")

    await bot.process_commands(message)


# responds with "yes." only to the bot admin
@bot.command(hidden=True)
async def yes(ctx):
    if await bot.is_owner(ctx.author):
        await ctx.send("yes.")


# closes the bot (only bot owners)
@bot.command(hidden=True)
async def cease(ctx):
    if await bot.is_owner(ctx.author):
        await ctx.send("Farewell...")
        print("Done.")

        await bot.close()
        sys.exit()


@bot.command(
    aliases=["information"],
    description="Displays information about the bot."
)
async def info(ctx):
    await ctx.send(
        "**Information:**\n"
        "Developer: ***brussels-sprout***\n"
        "Github: *https://github.com/brussels-sprout/rice_pudding*"
    )


bot.remove_command("help")


@bot.command(name="help", description="Displays the help message.")
async def _help(ctx, specific_name=None):
    if not specific_name:
        command_list = []
        for command in bot.commands:
            if command.hidden is False:
                if command.brief is not None:
                    command_list.append(f"{command} - {command.brief}")
                else:
                    command_list.append(f"{command} - {command.description}")

        command_text = "\n".join(command_list)

        await ctx.send(
            "```\n"
            "Help message:\n\n"
            f"{command_text}"
            "\n```"
        )
    else:
        commands_dictionary = {}
        for command in bot.commands:
            commands_dictionary.update({command.name: command})

        if specific_name in commands_dictionary.keys():
            command = commands_dictionary[specific_name]
            if command.hidden is False:
                await ctx.send(
                    "```\n"
                    f"{command.name} command help message:\n\n"
                    f"{command.description}"
                    "\n```"
                )
            else:
                await ctx.send("**Error:** unknown command.")
        else:
            await ctx.send("**Error:** unknown command.")


@bot.command(
    aliases=["latency"],
    description="Displays the bot's ping (in ms) to the server."
)
async def ping(ctx):
    latency = round(bot.latency, 3) * 1000  # in ms to 3 d.p.

    await ctx.send(f"Pong! ({latency}ms)")


@bot.command(
    name="8ball",
    description="Plays the game eight-ball (8ball)."
)
# func name cannot start with a number
async def _8ball(ctx, *, arg):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    question = arg
    choice = random.choice(responses)

    await ctx.send(
        f"**Question:** *{question}*\n"
        f"**Response:** {choice}"
    )


translator = Translator()


@bot.command(
    name="translate",
    brief="Translates text.",
    description="Translates text.\nFormat: [from] [to] [text]"
)
async def _translate(ctx, source_lang, destination_lang, text):
    try:
        if source_lang == "auto":
            translated = translator.translate(
                text,
                destination_lang
            ).text
        else:
            translated = translator.translate(
                text,
                destination_lang,
                source_lang
            ).text

        await ctx.send(
            f"**Input:** {text} *({source_lang})*\n"
            f"**Output:** {translated} *({destination_lang})*"
        )
    except ValueError as error:
        await ctx.send(f"**Error:** {error}.")


bot.run(TOKEN)
