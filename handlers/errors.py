import discord
from discord.ext import commands
from utils.embed_builder import EmbedBuilder
from utils.logger import setup_logger

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger()
        self.embed_builder = EmbedBuilder()

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        self.logger.error(f"Global error in event {event}: {args} {kwargs}")
        if args and isinstance(args[0], discord.Interaction):
            await args[0].response.send_message(embed=self.embed_builder.error("An unexpected error occurred"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=self.embed_builder.error("Command not found"))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=self.embed_builder.error("You don't have permission to use this command"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=self.embed_builder.error(f"Missing argument: {error.param}"))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=self.embed_builder.error(f"Invalid argument: {error}"))
        else:
            self.logger.error(f"Command error: {error}")
            await ctx.send(embed=self.embed_builder.error(f"An error occurred: {error}"))

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))