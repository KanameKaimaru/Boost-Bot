import discord
from discord.ext import commands
from commands.stock import add_stock, view_stock, remove_stock
import json
import os
from utils.embed_builder import EmbedBuilder

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {config_path}")

class StockManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.embed_builder = EmbedBuilder()

    @commands.hybrid_command(name="add_stock", description="Add tokens to stock")
    async def add_stock_cmd(self, ctx: commands.Context, month: int, tokens: str):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await add_stock(ctx, month, tokens)

    @commands.hybrid_command(name="view_stock", description="View current stock")
    async def view_stock_cmd(self, ctx: commands.Context):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await view_stock(ctx)

    @commands.hybrid_command(name="remove_stock", description="Remove tokens from stock")
    async def remove_stock_cmd(self, ctx: commands.Context, month: int, quantity: int):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await remove_stock(ctx, month, quantity)

    def _has_permissions(self, ctx):
        return (
            str(ctx.author.id) in self.config["permissions"]["owners_ids"] or
            any(str(role.id) in self.config["permissions"]["admin_role_ids"] for role in ctx.author.roles)
        )

async def setup(bot):
    await bot.add_cog(StockManagement(bot))