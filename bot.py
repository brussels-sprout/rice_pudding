# rice_pudding
# by brussels_sprout


import sys
import os

# import discord
from discord.ext import commands
import logging
import dotenv
import random
from googletrans import Translator


def choose_logger():
    choice = input(
        "Log to file (all levels) or"
        " to console (warnings and higher)? (f/c) - "
    ).lower().strip()
    if choice == "f":
        # logs all levels to a file called "discord.log"
        logger = logging.getLogger("discord")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            filename="discord.log",
            encoding="utf-8",
            mode="w"
        )
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
            )
        )
        logger.addHandler(handler)
    elif choice == "c":
        # logs warnings and higher levels to console
        logging.basicConfig(level=logging.WARNING)
    else:
        print("Invalid input, try again.")
        choose_logger()


choose_logger()


def handle_token():
    choice = input(
        "Has token not been set or changed? (y/n) - "
    ).lower().strip(" ")
    if choice == "y":
        current_os = sys.platform
        if current_os == "win32":
            token_input = input("Input Discord bot token: ").strip(" ")
            cwd = os.getcwd()

            # creates a file called ".env" containing the token
            os.system(
                f"cmd /c cd {cwd} & echo token={token_input} > .env"
            )

            del token_input
        else:
            # will probably add support for linux later
            print("Unsupported operating system.")
            sys.exit()
    elif choice == "n":
        pass
    else:
        print("Invalid input, try again.")
        handle_token()

    dotenv.load_dotenv()

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
        f"{bot.user.name}'s prefix: \"{prefix}\" (example: *{prefix}help*)"
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


# closes the bot (only bot admin)
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
            if command.hidden is not True:
                if command.brief is not None:
                    command_list.append(f"{command} - {command.brief}")
                else:
                    command_list.append(f"{command} - {command.description}")

        command_text = "\n".join(command_list)

        await ctx.send(
            "```\n"
            f"{bot.user.name}'s command:\n\n"
            f"{command_text}"
            "\n```"
        )
    else:
        commands_dictionary = {}
        for command in bot.commands:
            commands_dictionary.update({command.name: command})

        if specific_name in commands_dictionary.keys():
            await ctx.send(
                "```\n"
                f"{bot.user.name}'s {specific_name} commands:\n\n"
                f"{commands_dictionary[specific_name].description}"
                "\n```"
            )
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
