from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import discord
from data import data_handler


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="logchannel", description="Set the log channel for the bot")
    async def logchannel(self, ctx: SlashContext, channel: discord.TextChannel):

        # check if user has valid permissions, and if the channel specified is a text channel.
        exc: discord.Member = channel.guild.get_member(ctx.author_id)

        if not exc.guild_permissions.administrator:
            return

        if type(channel) == discord.TextChannel:
            data_handler.set_log_channel(ctx.guild.id, channel.id)
            await ctx.send(f"Channel set to {channel.mention}")
        else:
            await ctx.send(f"You must specify a text channel.")


def setup(bot):
    bot.add_cog(Slash(bot))
