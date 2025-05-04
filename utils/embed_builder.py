import discord
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
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

class EmbedBuilder:
    def __init__(self):
        self.config = load_config()
        self.default_color = 0x2F3136
        self.error_color = 0xFF0000
        self.success_color = 0x00FF00
        self.info_color = 0x00BBFF

    def error(self, description: str, title: str = "Error"):
        embed = discord.Embed(
            title=title,
            description=description,
            color=self.error_color,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Boost Bot | Powered by かいまる")
        return embed

    def success(self, description: str, title: str = "Success"):
        embed = discord.Embed(
            title=title,
            description=description,
            color=self.success_color,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Boost Bot | Powered by かいまる")
        embed.set_thumbnail(url=self.config["customization"]["thumbnail"])
        return embed

    def info(self, description: str, title: str = "Information"):
        embed = discord.Embed(
            title=title,
            description=description,
            color=self.info_color,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Boost Bot | Powered by かいまる")
        return embed

    def webhook(self, description: str, title: str = "Webhook Log"):
        embed = DiscordEmbed(
            title=title,
            description=description,
            color=self.default_color
        )
        embed.set_footer(text="Boost Bot | Powered by かいまる")
        return embed

    def send_webhook(self, url: str, embed: DiscordEmbed):
        webhook = DiscordWebhook(url=url, content="")
        webhook.add_embed(embed)
        response = webhook.execute()
        if response.status_code not in range(200, 207):
            print(f"Failed to send webhook: {response.status_code}")