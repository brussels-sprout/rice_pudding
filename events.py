# rice_pudding
# by brussels_sprout

import config

bot = config.bot


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
