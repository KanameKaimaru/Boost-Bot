import discord
from discord.ext import commands
from commands.boost import BoostModal, getinviteCode, checkInvite, getStock, remove
from utils.booster import Booster
from utils.embed_builder import EmbedBuilder
from config.config import load_config

class Boosting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.embed_builder = EmbedBuilder()

    @commands.hybrid_command(name="boost", description="Boost a server with tokens")
    async def boost(self, ctx: commands.Context):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await ctx.send_modal(BoostModal())

    def _has_permissions(self, ctx):
        return (
            str(ctx.author.id) in self.config["permissions"]["owners_ids"] or
            any(str(role.id) in self.config["permissions"]["admin_role_ids"] for role in ctx.author.roles)
        )

async def setup(bot):
    await bot.add_cog(Boosting(bot))