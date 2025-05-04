import discord
from discord.ext import commands
import json
import os
from utils.embed_builder import EmbedBuilder
from utils.logger import setup_logger

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {config_path}")

class WebhookHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.embed_builder = EmbedBuilder()
        self.logger = setup_logger()

    async def send_webhook_log(self, title: str, description: str):
        if not self.config["webhook"]["use_log"]:
            return
        
        embed = self.embed_builder.webhook(title, description)
        self.embed_builder.send_webhook(self.config["webhook"]["url"], embed)
        self.logger.info(f"Sent webhook log: {title}")

async def setup(bot):
    await bot.add_cog(WebhookHandler(bot))