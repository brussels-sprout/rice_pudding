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


def logging_setup():
    # # logs all levels (debug and higher) to a file called "discord.log"
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    #     filename="discord.log",
    #     filemode="w"
    # )
    #
    # # logs warnings and higher levels to console
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.WARNING)
    # console_handler.setFormatter(
    #     logging.Formatter(
    #         "%(asctime)s - %(levelname)s - %(name)s: %(message)s"
    #     )
    # )
    # logging.getLogger("").addHandler(console_handler)

    logger = logging.getLogger("discord")

    file_handler = logging.FileHandler(
        filename="discord.log",
        encoding="utf-8",
        mode="a"
    )
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s: %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # formatter = logging.Formatter(
    #     "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
    # )
    #
    # # logs all levels (debug and higher) to a file called "discord.log"
    # file_logger = logging.getLogger("discord")
    # file_logger.setLevel(logging.DEBUG)
    # file_handler = logging.FileHandler(
    #     filename="discord.log",
    #     encoding="utf-8",
    #     mode="w"
    # )
    # file_handler.setFormatter(formatter)
    # file_logger.addHandler(file_handler)
    #
    # # logs warnings and higher levels to console
    # console_logger = logging.StreamHandler()
    # console_logger.setLevel(logging.WARNING)


logging_setup()


def check_environment():
    global on_heroku

    if "DYNO" in os.environ:
        on_heroku = True
    else:
        on_heroku = False


def handle_token():
    if not on_heroku:
        choice = input(
            "Has token changed or NOT been set? (y/n) - "
        ).lower().strip(" ")

        if choice in ("y", "yes"):
            # sys.platform is current OS
            if sys.platform in ("win32", "linux", "darwin"):
                token_input = input("Input Discord bot token: ").strip(" ")
                cwd = os.getcwd()

                # creates a file called ".env" containing the bot token
                os.system(f"cmd /c cd {cwd} & echo TOKEN={token_input} > .env")

                del token_input
            else:
                print("Unsupported operating system.")
                sys.exit()
        elif choice in ("n", "no"):
            pass
        else:
            print("Invalid input, try again.")
            handle_token()

        dotenv.load_dotenv()

    global TOKEN
    TOKEN = os.environ["TOKEN"]


on_heroku = None
check_environment()


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


# responds with "yes." only to the bot owners
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
