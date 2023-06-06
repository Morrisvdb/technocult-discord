import os

"""Imports the client from init.py"""
from init import bot

for f in os.listdir("./cogs"):
    if f.endswith(".py"):
        bot.load_extension(f"cogs.{f[:-3]}")
        print("loaded cog")

bot.run(os.environ.get("TOKEN"))
