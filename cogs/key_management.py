import discord
from discord.ext import commands
from commands.key_commands import (
    KeyCreationModal, KeyRequestModal, KeyFilterModal,
    delete_keys, get_key_information, key_stats, get_used_key_information,
    get_key, delete_key
)
from config.config import load_config
from utils.embed_builder import EmbedBuilder

class KeyManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.embed_builder = EmbedBuilder()

    @commands.hybrid_command(name="new_keys", description="Create new keys for boosting")
    async def new_keys(self, ctx: commands.Context):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await ctx.send_modal(KeyCreationModal())

    @commands.hybrid_command(name="get_all_keys", description="Get all keys in the system")
    async def get_all_keys(self, ctx: commands.Context):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await ctx.send_modal(KeyRequestModal())

    @commands.hybrid_command(name="get_keys", description="Get specific keys by month and amount")
    async def get_keys(self, ctx: commands.Context):
        if not self._has_permissions(ctx):
            await ctx.send(embed=self.embed_builder.error("You are not authorized to use this command"))
            return
        await ctx.send_modal(KeyFilterModal())

    @commands.hybrid_command(name="delete_keys", description="Delete keys from the system")
    async def delete_keys_cmd(self, ctx: commands.Context, month: int, amount: int, quantity: int, delete_all: bool = False):
        await delete_keys(ctx, month, amount, quantity, delete_all)

    @commands.hybrid_command(name="get_key_information", description="Get information about a specific key")
    async def get_key_info(self, ctx: commands.Context, key: str):
        await get_key_information(ctx, key)

    @commands.hybrid_command(name="key_stats", description="Show key statistics")
    async def key_stats_cmd(self, ctx: commands.Context):
        await key_stats(ctx)

    @commands.hybrid_command(name="get_used_key_information", description="Get information about a used key")
    async def get_used_key_info(self, ctx: commands.Context, key: str):
        await get_used_key_information(ctx, key)

    @commands.hybrid_command(name="get_key", description="Get a key by month and amount")
    async def get_key_cmd(self, ctx: commands.Context, month: int, amount: int):
        await get_key(ctx, month, amount)

    @commands.hybrid_command(name="delete_key", description="Delete a specific key")
    async def delete_key_cmd(self, ctx: commands.Context, key: str):
        await delete_key(ctx, key)

    def _has_permissions(self, ctx):
        return (
            str(ctx.author.id) in self.config["permissions"]["owners_ids"] or
            any(str(role.id) in self.config["permissions"]["admin_role_ids"] for role in ctx.author.roles)
        )

async def setup(bot):
    await bot.add_cog(KeyManagement(bot))