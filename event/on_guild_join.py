from discord.ext import commands
import discord
import log


class on_guild_join(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        log.log(f"Joined guild {guild.name} ({guild.id}); Owner is {guild.owner}")


def setup(bot):
    bot.add_cog(on_guild_join(bot))
