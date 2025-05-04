import discord
from discord import DiscordWebhook, DiscordEmbed
from config.config import load_config

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