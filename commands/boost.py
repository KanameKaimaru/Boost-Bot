import discord
import time
from utils.booster import Booster
from utils.embed_builder import EmbedBuilder
import json
import os
import requests

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

def getinviteCode(inv):
    if "discord.gg" in inv:
        return inv.split("discord.gg/")[1]
    if "https://discord.gg" in inv:
        return inv.split("https://discord.gg/")[1]
    if "discord.com/invite" in inv:
        return inv.split("discord.com/invite/")[1]
    if "https://discord.com/invite/" in inv:
        return inv.split("https://discord.com/invite/")[1]
    return inv

def checkInvite(invite: str):
    data = requests.get(
        f"https://discord.com/api/v9/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true"
    ).json()
    return data["guild"]["id"] if data.get("code") != 10006 else False

def getStock(filename: str):
    tokens = []
    with open(filename, "r") as file:
        for line in file.read().splitlines():
            tokens.append(line.split(":")[2] if ":" in line else line)
    return tokens

def remove(token: str, filename: str):
    tokens = getStock(filename)
    tokens.pop(tokens.index(token))
    with open(filename, "w") as file:
        for x in tokens:
            file.write(f"{x}\n")

class BoostModal(discord.ui.Modal, title="Boost Server"):
    invite = discord.ui.TextInput(
        label="Invite",
        placeholder="Enter server invite code",
        required=True,
        style=discord.TextStyle.short
    )
    amount = discord.ui.TextInput(
        label="Amount",
        placeholder="Number of boosts (even numbers)",
        required=True,
        style=discord.TextStyle.short
    )
    months = discord.ui.TextInput(
        label="Months",
        placeholder="1 or 3 months",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        try:
            amount = int(self.amount.value)
            months = int(self.months.value)
            invite = self.invite.value
        except ValueError:
            await interaction.followup.send(embed=embed_builder.error("Invalid input. Please use numbers for amount and months"))
            return

        if amount % 2 != 0:
            await interaction.followup.send(embed=embed_builder.error("Number of boosts must be even"))
            return
        if months not in [1, 3]:
            await interaction.followup.send(embed=embed_builder.error("Months must be 1 or 3"))
            return

        invite_code = getinviteCode(invite)
        invite_data = checkInvite(invite_code)
        if not invite_data:
            await interaction.followup.send(embed=embed_builder.error(f"Invalid invite: .gg/{invite_code}"))
            return

        filename = f"data/{months}m.txt"
        tokens_stock = getStock(filename)
        required_stock = amount // 2

        if required_stock > len(tokens_stock):
            await interaction.followup.send(embed=embed_builder.error("Not enough tokens in stock. Use /restock"))
            return

        boost = Booster()
        tokens = [tokens_stock.pop(0) for _ in range(required_stock)]
        for token in tokens:
            remove(token, filename)

        await interaction.followup.send(embed=embed_builder.info("Joining and boosting..."))
        start = time.time()
        status = boost.thread(invite_code, tokens, invite_data)
        time_taken = round(time.time() - start, 2)

        embed = embed_builder.success(
            title="Boost Results",
            description=(
                f"**Amount:** {amount} {months}m Boosts\n"
                f"**Tokens:** {required_stock}\n"
                f"**Server:** .gg/{invite_code}\n"
                f"**Successful Boosts:** {len(status['success'])*2}\n"
                f"**Failed Boosts:** {len(status['failed'])*2}\n"
                f"**Captcha:** {len(status['captcha'])*2}\n"
                f"**Time Taken:** {time_taken}s\n\n"
                f"**Success Tokens:** ```{status['success']}```\n"
                f"**Failed Tokens:** ```{status['failed']}```\n"
                f"**Captcha Tokens:** ```{status['captcha']}```"
            )
        )
        await interaction.followup.send(embed=embed)

        if config["webhook"]["use_log"]:
            embed = embed_builder.webhook(
                title="Boosting Data",
                description=(
                    f"**Amount:** {amount} {months}m Boosts\n"
                    f"**Tokens:** {required_stock}\n"
                    f"**Server:** .gg/{invite_code}\n"
                    f"**Successful:** {len(status['success'])*2}\n"
                    f"**Failed:** {len(status['failed'])*2}\n"
                    f"**Time Taken:** {time_taken}s\n"
                    f"**Failed Tokens:** ```{status['failed']}```\n"
                    f"**Captcha Tokens:** ```{status['captcha']}```\n"
                    f"**Success Tokens:** ```{status['success']}```"
                )
            )
            embed_builder.send_webhook(config["webhook"]["url"], embed)

        if config["customization"]["enabled"]:
            boost.humanizerthread(tokens=status["success"])