import discord
import json
from utils.authsystem import generate_key, load_keys_from_file, save_keys_to_file
from utils.embed_builder import EmbedBuilder
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

config = load_config()
embed_builder = EmbedBuilder()

class KeyCreationModal(discord.ui.Modal, title="Create Keys"):
    month = discord.ui.TextInput(
        label="Month",
        placeholder="1 or 3",
        required=True,
        style=discord.TextStyle.short
    )
    amount = discord.ui.TextInput(
        label="Amount",
        placeholder="Number of boosts",
        required=True,
        style=discord.TextStyle.short
    )
    quantity = discord.ui.TextInput(
        label="Quantity",
        placeholder="Number of keys to create",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            month = int(self.month.value)
            amount = int(self.amount.value)
            quantity = int(self.quantity.value)
        except ValueError:
            await interaction.response.send_message(embed=embed_builder.error("Invalid input. Please use numbers"))
            return

        keys = load_keys_from_file("data/keys/keys.json")
        generate_key(keys, month, amount, quantity, "data/keys/keys.json")
        
        await interaction.response.send_message(embed=embed_builder.success(
            f"Successfully created {quantity} keys for {amount}x {month} month boosts",
            "Key Creation"
        ))

class KeyRequestModal(discord.ui.Modal, title="Request All Keys"):
    async def on_submit(self, interaction: discord.Interaction):
        try:
            with open("data/keys/keys.json", "rb") as file:
                await interaction.user.send(file=discord.File(file, "keys.txt"))
                await interaction.response.send_message(embed=embed_builder.success(
                    "Keys sent to your DMs",
                    "Key Request"
                ))
        except FileNotFoundError:
            await interaction.response.send_message(embed=embed_builder.error("No keys found"))

class KeyFilterModal(discord.ui.Modal, title="Filter Keys"):
    month = discord.ui.TextInput(
        label="Month",
        placeholder="1 or 3",
        required=True,
        style=discord.TextStyle.short
    )
    amount = discord.ui.TextInput(
        label="Amount",
        placeholder="Number of boosts",
        required=True,
        style=discord.TextStyle.short
    )
    quantity = discord.ui.TextInput(
        label="Quantity",
        placeholder="Number of keys",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            month = int(self.month.value)
            amount = int(self.amount.value)
            quantity = int(self.quantity.value)
        except ValueError:
            await interaction.response.send_message(embed=embed_builder.error("Invalid input. Please use numbers"))
            return

        with open("data/keys/keys.json", "r") as file:
            all_keys = json.load(file)
        
        filtered_keys = [key for key in all_keys if key['month'] == month and key['amount'] == amount]
        if len(filtered_keys) < quantity:
            await interaction.response.send_message(embed=embed_builder.error("Not enough keys found"))
            return

        keys_to_send = filtered_keys[:quantity]
        keys_str = '\n'.join(key['key'] for key in keys_to_send)
        
        with open("data/keys/filtered_keys.txt", "w") as file:
            file.write(keys_str)
        
        with open("data/keys/filtered_keys.txt", "rb") as file:
            await interaction.user.send(file=discord.File(file, "filtered_keys.txt"))
        
        await interaction.response.send_message(embed=embed_builder.success(
            "Filtered keys sent to your DMs",
            "Key Filter"
        ))

async def delete_keys(ctx, month: int, amount: int, quantity: int, delete_all: bool = False):
    if not _has_permissions(ctx):
        await ctx.send(embed=embed_builder.error("You are not authorized to use this command"))
        return
    
    try:
        with open("data/keys/keys.json", "r") as file:
            all_keys = json.load(file)
        
        if delete_all:
            all_keys = []
        else:
            filtered_keys = [key for key in all_keys if key['month'] == month and key['amount'] == amount]
            if len(filtered_keys) < quantity:
                await ctx.send(embed=embed_builder.error("Not enough keys found"))
                return
            all_keys = [key for key in all_keys if key not in filtered_keys[:quantity]]
        
        save_keys_to_file(all_keys, "data/keys/keys.json")
        await ctx.send(embed=embed_builder.success("Keys deleted successfully", "Key Deletion"))
    except FileNotFoundError:
        await ctx.send(embed=embed_builder.error("No keys found"))

async def get_key_information(ctx, key: str):
    try:
        with open("data/keys/keys.json", "r") as file:
            all_keys = json.load(file)
        
        key_info = next((k for k in all_keys if k['key'] == key), None)
        if key_info:
            await ctx.send(embed=embed_builder.success(
                f"**Key:** {key_info['key']}\n**Month:** {key_info['month']}\n**Amount:** {key_info['amount']}",
                "Key Information"
            ))
        else:
            await ctx.send(embed=embed_builder.error("Key not found"))
    except FileNotFoundError:
        await ctx.send(embed=embed_builder.error("No keys found"))

async def key_stats(ctx):
    try:
        with open("data/keys/keys.json", "r") as file:
            all_keys = json.load(file)
        
        one_month = sum(1 for key in all_keys if key['month'] == 1)
        three_month = sum(1 for key in all_keys if key['month'] == 3)
        amount_stats = {}
        
        for key in all_keys:
            amount = key['amount']
            amount_stats[amount] = amount_stats.get(amount, 0) + 1
        
        stats = f"**1 Month Keys:** {one_month}\n**3 Month Keys:** {three_month}\n\n**Amount Stats:**\n"
        for amount, count in amount_stats.items():
            stats += f"{amount} boosts: {count} keys\n"
        
        await ctx.send(embed=embed_builder.success(stats, "Key Statistics"))
    except FileNotFoundError:
        await ctx.send(embed=embed_builder.error("No keys found"))

async def get_used_key_information(ctx, key: str):
    try:
        with open("data/keys/used_keys.json", "r") as file:
            all_keys = json.load(file)
        
        key_info = next((k for k in all_keys if k['key'] == key), None)
        if key_info:
            await ctx.send(embed=embed_builder.success(
                f"**Key:** {key_info['key']}\n**Month:** {key_info['month']}\n**Amount:** {key_info['amount']}\n"
                f"**Successful:** {key_info['successful']}\n**Failed:** {key_info['failed']}\n"
                f"**Time Taken:** {key_info['time_taken']}s\n**Invite:** {key_info['invite']}",
                "Used Key Information"
            ))
        else:
            await ctx.send(embed=embed_builder.error("Key not found"))
    except FileNotFoundError:
        await ctx.send(embed=embed_builder.error("No keys found"))

async def get_key(ctx, month: int, amount: int):
    if not _has_permissions(ctx):
        await ctx.send(embed=embed_builder.error("You are not authorized to use this command"))
        return
    
    try:
        with open("data/keys/keys.json", "r") as file:
            all_keys = json.load(file)
        
        filtered_keys = [key for key in all_keys if key['month'] == month and key['amount'] == amount]
        if not filtered_keys:
            await ctx.send(embed=embed_builder.error("No keys found for the specified criteria"))
            return
        
        key = filtered_keys[0]
        await ctx.send(embed=embed_builder.success(
            f"**Month:** {key['month']}\n**Amount:** {key['amount']}\n**Key:** {key['key']}",
            "Filtered Key"
        ))
    except FileNotFoundError:
        await ctx.send(embed=embed_builder.error("No keys found"))

async def delete_key(ctx, key: str):
    if not _has_permissions(ctx):
        await ctx.send(embed=embed_builder.error("You are not authorized to use this command"))
        return
    
    try:
        with open("data/keys/keys.json", "r") as file:
            all_keys = json.load(file)
        
        filtered_keys = [k for k in all_keys if k['key'] == key]
        if not filtered_keys:
            await ctx.send(embed=embed_builder.error("Key not found"))
            return
        
        all_keys = [k for k in all_keys if k['key'] != key]
        save_keys_to_file(all_keys, "data/keys/keys.json")
        await ctx.send(embed=embed_builder.success(f"Key {key} deleted successfully", "Key Deletion"))
    except FileNotFoundError:
        await ctx.send(embed=embed_builder.error("No keys found"))

def _has_permissions(ctx):
    return (
        str(ctx.author.id) in config["permissions"]["owners_ids"] or
        any(str(role.id) in config["permissions"]["admin_role_ids"] for role in ctx.author.roles)
    )