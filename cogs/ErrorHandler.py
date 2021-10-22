from discord.ext import commands

class ErrorHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.UserInputError):
            message = 'Beep Beep! Your input is wrong ¯\_(ツ)_/¯ ' 
        
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)

def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
