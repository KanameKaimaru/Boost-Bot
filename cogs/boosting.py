import discord
from discord.ext import commands
from commands.boost import BoostModal, getinviteCode, checkInvite, getStock, remove
from utils.booster import Booster
from utils.embed_builder import EmbedBuilder
import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {config_path}")

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