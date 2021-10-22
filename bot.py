import discord
import logging

from discord.ext import commands, tasks

from cogs.web               import WebStatus
from cogs.convert_pdf       import Convert
from cogs.cmd_error_handler import ErrorHandler

from datetime   import date, datetime
from dotenv     import load_dotenv
import os

# Save logger debug events to file---------------------------------------------------------

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# -----------------------------------------------------------------------------------------

intents = discord.Intents.all()
prefix='-'

bot = commands.Bot(
    command_prefix=prefix,
    intents=intents
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')   

@tasks.loop(hours=8)
async def continuously_check_for_update():
    current_time = datetime.now()
    time_format = "%d/%m/%Y %H:%M:%S"
    ###
    today_date = date.today()
    date_format = "%d-%m-%Y"

    path_to = f"Schedule_{today_date.strftime(date_format)}.pdf"
    channel_id = 897232495244881961

    if WebStatus.check_if_updated() is True:
        WebStatus.download(path_to)
        Convert.conversion_to_jpg(path_to)

        # Array of files
        schedule_files = [
            discord.File('Schedule_0.jpg'),
            discord.File('Schedule_1.jpg'),
            discord.File(path_to)
        ]

        try:
            channel = bot.get_channel(channel_id)
            await channel.send(files=schedule_files)
            await channel.send(f"Modified at: ***{WebStatus.last_modified()}***")
            await WebStatus.remove_file()
        except Exception as e:
            print(f"continuously_check_for_update() - Error occurred: {e}")
    
    else:
        print(f"No update: {current_time.strftime(time_format)}")

bot.add_cog(ErrorHandler(bot))

@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")


@bot.command(name='last')
async def check(ctx):
    await ctx.send(WebStatus.last_modified())

continuously_check_for_update.start()

load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))