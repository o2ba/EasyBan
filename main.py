import discord
from discord.ext import commands
import datetime
from discord_slash import SlashCommand, SlashContext
import log

bot = commands.Bot(command_prefix="eb!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True, override_type=True)


@bot.event
async def on_ready():
    log.log("Bot is ready")
    print("-------------------------------------------------")
    print("EB BOT IS READY @ ", datetime.datetime.today())
    print("-------------------------------------------------")
    status = discord.Game(name="Using slash commands")
    await bot.change_presence(activity=status)


if __name__ == '__main__':
    # List of extensions
    extensions = ['command.logchannel', 'event.on_guild_join', 'event.on_user_join', 'event.on_reaction_add']

    # Load extensions
    for ex in extensions:
        bot.load_extension(ex)

    with open("token", "r") as t:
        bot.run(t.read())
