import discord

from discord.ext import commands, tasks
import logging

from cogs import (
    web,
    convert_pdf,
    cmd_error_handler
)

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

class Bot(commands.Bot):

    def __init__(self, prefix='-'):
        super(Bot, self).__init__(command_prefix=prefix, intents=discord.Intents.all())


    async def on_ready(self):
        print(f'Logged in as {self.user.name}')   

    @tasks.loop(hours=8)
    async def continuously_check_for_update():
        current_time = datetime.now()
        time_format = "%d/%m/%Y %H:%M:%S"
        ###
        today_date = date.today()
        date_format = "%d-%m-%Y"

        path_to = f"Schedule_{today_date.strftime(date_format)}.pdf"
        channel_id = 897232495244881961

        if web.WebStatus.check_if_updated() is True:
            web.WebStatus.download(path_to)
            convert_pdf.Convert.conversion_to_jpg(path_to)

            # Array of files
            schedule_files = [
                discord.File('Schedule_0.jpg'),
                discord.File('Schedule_1.jpg'),
                discord.File(path_to)
            ]

            try:
                channel = bot.get_channel(channel_id)
                await channel.send(files=schedule_files)
                await channel.send(f"Modified at: ***{web.WebStatus.last_modified()}***")
                await web.WebStatus.remove_file()
            except Exception as e:
                print(f"continuously_check_for_update() - Error occurred: {e}")
        
        else:
            print(f"No update: {current_time.strftime(time_format)}")

    bot.add_cog(cmd_error_handler.ErrorHandler(bot))

    @bot.command()
    async def ping(ctx):
	    await ctx.channel.send("pong")

    
    @bot.command(name='last')
    async def check(ctx):
        await ctx.send(web.WebStatus.last_modified())
        

    continuously_check_for_update.start()


if __name__ == '__main__':
    bot = Bot()
     
    load_dotenv()
    bot.run(os.getenv("DISCORD_TOKEN"))