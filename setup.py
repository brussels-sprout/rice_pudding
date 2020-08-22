# rice_pudding
# by brussels_sprout

import sys
import os

import config

# see line 61
import logging


def logging_setup():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(
        filename="discord.log",
        encoding="utf-8",
        mode="a"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s: %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


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

        from dotenv import load_dotenv

        load_dotenv()

    config.TOKEN = os.environ["TOKEN"]


logging_setup()

on_heroku = None
check_environment()

handle_token()
