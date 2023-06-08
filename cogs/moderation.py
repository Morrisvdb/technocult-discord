import discord
from discord import Option, guild_only
from discord.ext import commands
import sqlalchemy.exc
"""Import other functions"""
from init import bot, db, db_error, channelTypes
from models import Channel, Typo
import re


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="remove-typo", description="Remove a typo from the typo channel.", guild_ids=[977513866097479760, 1047234879743611034])
    @guild_only()
    async def removeTypo(self, ctx: discord.ApplicationContext,
                         link: Option(input_type=str, description="The message that contains the typo.", required=True),
                         block: Option(input_type=str, description="Whether or not to block this typo form being registered again.", required=False, choices=["yes", "no"])):
        typoChannel = db.query(Channel).filter_by(
            guild_id=ctx.guild.id, channel_id=ctx.channel.id, channel_type="typo").first()
        if typoChannel is None:
            doesNotExistEmbed = discord.Embed(
                title="Command is disabled in this server!",
                description="""This command has been disabled in this server because there is no channel marked as a typo channel. \n Consult an admin if you think this is a mistake.""",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=doesNotExistEmbed)
        else:
            typo = db.query(Typo).filter_by(message_url=link).first()
            if typo is None:
                doesNotExistEmbed = discord.Embed(
                    title="Typo not found!",
                    description="""The typo you are trying to remove was not registered in the database.""",
                    color=discord.Color.orange()
                )
                await ctx.respond(embed=doesNotExistEmbed)
            else:
                print("Ping")
                if block == "yes":
                    typo.blocked = True
                    db.add(typo)
                else:
                    db.delete(typo)
                db.commit()
                typoPublicMessage = await bot.get_channel(typoChannel.channel_id).fetch_message(typo.public_msg_id)
                print("Ping")
                await typoPublicMessage.delete()
                removedEmbed = discord.Embed(
                    title="Typo removed!",
                    description="""The typo has been removed from the typo channel.""",
                    color=discord.Color.green()
                )
                await ctx.respond(embed=removedEmbed)
def setup(bot):
    bot.add_cog(Moderation(bot))
