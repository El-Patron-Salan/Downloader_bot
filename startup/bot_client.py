from discord.ext import commands

class BotClient(commands.Bot):

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')