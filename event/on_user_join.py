from discord.ext import commands
from datetime import date
from variables import cfg as evar
import discord
import data.data_handler as d
import log


class on_user_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # fetch log channel for said server, if returns None log error
        log_channel = d.get_log_channel(member.guild.id)
        if log_channel is not None:
            # Get channel ctx
            ctx = member.guild.get_channel(log_channel)

            # create embed
            new_embed = join_handler(member)

            # if ctx is invalid (NoneType), we will get AttributeError, if permissions not sufficient, we will
            # get forbidden
            try:
                msg = await ctx.send(f"Member {member.mention} joined the server", embed=new_embed.fill_embed())
                await self.add_reactions(msg)
            except AttributeError:
                log.warning(f"Invalid channel for guild {member.guild.name} ({member.guild.id}); "
                            f"Owner {member.guild.owner}")
            except discord.errors.Forbidden:
                log.warning(f"Invalid permissions for guild {member.guild.name} ({member.guild.id}); "
                            f"Owner {member.guild.owner}")

    async def add_reactions(self, message: discord.Message):
        try:
            reaction = self.bot.get_emoji(evar.ban_emoji)
            reaction2 = self.bot.get_emoji(evar.kick_emoji)
            await message.add_reaction(reaction)
            await message.add_reaction(reaction2)
        except discord.Forbidden:
            await message.channel.send("[ERROR] Cannot react to message. Please check I have sufficient permissions")


class join_handler:
    def __init__(self, member: discord.Member):
        self.member = member
        self.guild = member.guild

    def init_embed(self) -> discord.Embed:
        return discord.Embed(color=evar.embedColor,
                             title=evar.embedTitle,
                             url=evar.embedURL). \
            set_thumbnail(url=self.member.avatar_url). \
            set_footer(text=evar.embedFooter)

    def fill_embed(self) -> discord.Embed:
        embed = self.init_embed()

        # Init Embed
        embed = discord.Embed(color=evar.embedColor, title=evar.embedTitle,
                              url=evar.embedURL).set_thumbnail(
            url=self.member.avatar_url).set_footer(text=evar.embedFooter)

        # Add field values
        embed.add_field(name="User Details",
                        value=f"User {self.member.name}#{self.member.discriminator} "
                              f"joined the server. Their user ID is {self.member.id}",
                        inline=False)

        # get platform
        platform = self.find_platform()

        # Add to embed if platform not null
        if platform is not None:
            embed.add_field(name="Platform",
                            value=f"They are most likely using {platform} "
                                  f"to access discord at this time",
                            inline=False)

        # get account age in days
        # TODO increment to months, years
        account_age = (date.today() - self.member.created_at.date()).days

        embed.add_field(name="Account Age",
                        value=f"Their account was created {account_age} "
                              f"days ago",
                        inline=False)

        return embed

    def find_platform(self) -> str or None:

        if self.member.is_on_mobile():
            return "a mobile phone"

        if self.member.desktop_status == "online" and self.member.web_status == "offline":
            return "a desktop computer"

        if self.member.desktop_status == "offline" and self.member.web_status == "online":
            return "a browser"

        return None


def setup(bot):
    bot.add_cog(on_user_join(bot))
