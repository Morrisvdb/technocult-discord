import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from discord.ext import commands
import discord

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
Base = declarative_base()

# TOKEN = os.environ["DISCORD_TOKEN"]
bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")


async def db_error(ctx):
    """Sends an embed to the user when there is an error with the database."""
    embed = discord.Embed(
        title="Database Error!",
        description="""There was an error with the database.
        Try again, or contact the bot owner to resolve this issue.""",
        color=discord.Color.red()
    )
    db.rollback()
    await ctx.send(embed=embed)
