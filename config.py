# rice_pudding
# by brussels_sprout

# TOKEN is set in setup.py
TOKEN = None

bot = None


def set_bot():
    from discord.ext import commands

    global bot
    bot = commands.Bot(command_prefix="h!")


set_bot()
