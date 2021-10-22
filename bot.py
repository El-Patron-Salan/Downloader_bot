import discord

from discord.ext import commands, tasks


from cogs import (
    web,
    convert_pdf,
    ErrorHandler
)

from datetime import date, datetime
from dotenv import load_dotenv
import os


class Bot(commands.Bot):

    def __init__(self, prefix="-"):
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
            convert_pdf(path_to)

            # Array of files
            schedule_files = [
                discord.File('Schedule_0.jpg'),
                discord.File('Schedule_1.jpg'),
                discord.File(path_to)
            ]

            try:
                channel = bot.get_channel(channel_id)
                await channel.send(files=schedule_files)
                await web.WebStatus.remove_file
            except Exception as e:
                print(f"continuously_check_for_update() - Error occurred: {e}")
        
        else:
            print(f"No update: {current_time.strftime(time_format)}")

    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content == '-check':
            await message.channel.send(web.WebStatus.last_modified())


    continuously_check_for_update.start()


if __name__ == '__main__':
     bot = Bot()
     load_dotenv()
     bot.run(os.getenv("DISCORD_TOKEN"))