from discord.ext import commands
import sys
import traceback
class ErrorHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Beep Beep! Command not found ¯\_(ツ)_/¯ ')
        if isinstance(error, commands.UserInputError):
            await ctx.send('Beep Beep! Your input is wrong ¯\_(ツ)_/¯ ')
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        


