import discord
from discord.ext import commands
from commands.auto_boost import start_auto_boost, stop_auto_boost, auto_boost_status
from config.config import load_config
from utils.embed_builder import EmbedBuilder

class AutoBoosting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.embed_builder = EmbedBuilder()

    @commands.hybrid_command(name="start_auto_boost", description="Start auto-boosting service")
    async def start_auto_boost_cmd(self, ctx: commands.Context):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await start_auto_boost(ctx)

    @commands.hybrid_command(name="stop_auto_boost", description="Stop auto-boosting service")
    async def stop_auto_boost_cmd(self, ctx: commands.Context):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await stop_auto_boost(ctx)

    @commands.hybrid_command(name="auto_boost_status", description="Check auto-boosting status")
    async def auto_boost_status_cmd(self, ctx: commands.Context):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await auto_boost_status(ctx)

    def _has_permissions(self, ctx):
        return (
            str(ctx.author.id) in self.config["permissions"]["owners_ids"] or
            any(str(role.id) in self.config["permissions"]["admin_role_ids"] for role in ctx.author.roles)
        )

async def setup(bot):
    await bot.add_cog(AutoBoosting(bot))