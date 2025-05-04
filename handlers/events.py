import discord
from discord.ext import commands
from config.config import load_config
from utils.logger import setup_logger

class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.logger = setup_logger()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=self.bot.embed_builder.error("You don't have permission to use this command"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=self.bot.embed_builder.error(f"Missing argument: {error.param}"))
        else:
            self.logger.error(f"Command error: {error}")
            await ctx.send(embed=self.bot.embed_builder.error(f"An error occurred: {error}"))

async def setup(bot):
    await bot.add_cog(EventHandler(bot))