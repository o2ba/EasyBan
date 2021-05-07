from discord.ext import commands
from datetime import date
import discord
import data.data_handler as d
import log
from variables import cfg as v


class added_reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reactor: discord.Member = payload.member

        if self.relevant_message(payload, message):
            user_in_bot_message = message.mentions[0]

            # If member has neither, we won't bother (efficiency)
            if reactor.guild_permissions.ban_members is False \
                    and reactor.guild_permissions.kick_members is False:
                return

            # If the user reacted with ban emoji
            if payload.emoji.id == v.ban_emoji and reactor.guild_permissions.ban_members is True:
                try:
                    dm = await user_in_bot_message.create_dm()
                    # TODO CUSTOM
                    await dm.send(f"You have been banned from {message.guild.name} by {reactor.mention}")
                    await user_in_bot_message.ban(reason=f"User banned by {reactor.name}#{reactor.discriminator}")
                    await message.edit(content=f"{message.content} [User banned by {reactor.mention}]")

                # If bot cannot ban
                except discord.Forbidden:
                    await message.channel.send("[ERROR] Missing Permission: Ban Members")
                # If user left
                except AttributeError:
                    await message.edit(content=f"[USER LEFT] {message.content}")

            # If the user reacted with kick emoji
            if payload.emoji.id == v.kick_emoji and reactor.guild_permissions.kick_members is True:
                try:
                    dm = await user_in_bot_message.create_dm()
                    # TODO CUSTOM
                    await dm.send(f"You have been kicked from {message.guild.name} by {reactor.mention}")
                    await user_in_bot_message.kick(reason=f"User kicked by {reactor.name}#{reactor.discriminator}")
                    await message.edit(content=f"{message.content} [User kicked by {reactor.mention}]")

                # If bot cannot ban
                except discord.Forbidden:
                    await message.channel.send("[ERROR] Missing Permission: Kick Members")
                # If user left
                except AttributeError:
                    await message.edit(content=f"[USER LEFT] {message.content}")

    def relevant_message(self, payload, message) -> bool:
        # Check if the reaction is relevant in the first place
        if payload.emoji.id not in [v.ban_emoji, v.kick_emoji]:
            return False
        # Check if the message reacted on has any mentions
        if len(message.mentions) == 0:
            return False
        # Make sure the person who reacted isn't the bot
        if payload.member.id == self.bot.user.id:
            return False
        # Make sure message author is the bot itself
        if message.author.id != self.bot.user.id:
            return False

        return True


def setup(bot):
    bot.add_cog(added_reaction(bot))
