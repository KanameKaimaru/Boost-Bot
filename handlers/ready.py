import discord
from discord.ext import commands
import json
import os
from utils.logger import setup_logger
from utils.onliner import onliner
import asyncio

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {config_path}")

class ReadyHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.logger = setup_logger()

    @commands.Cog.listener()
    async def on_ready(self):
        status_type = self.config["bot"]["status"]["type"]
        status_name = self.config["bot"]["status"]["name"]
        status_status = self.config["bot"]["status"]["status"]
        
        activity_types = {
            "playing": discord.Game,
            "streaming": discord.Streaming,
            "listening": discord.Activity,
            "watching": discord.Activity,
            "custom": discord.CustomActivity,
            "competing": discord.Activity
        }
        
        status_map = {
            "online": discord.Status.online,
            "dnd": discord.Status.dnd,
            "idle": discord.Status.idle,
            "invisible": discord.Status.invisible
        }
        
        activity_kwargs = {"name": status_name}
        if status_type == "streaming":
            activity_kwargs["url"] = self.config["bot"]["status"]["streaming_url"]
        elif status_type in ["listening", "watching", "competing"]:
            activity_kwargs["type"] = {
                "listening": discord.ActivityType.listening,
                "watching": discord.ActivityType.watching,
                "competing": discord.ActivityType.competing
            }[status_type]
        
        activity = activity_types.get(status_type, discord.Game)(**activity_kwargs)
        await self.bot.change_presence(
            status=status_map.get(status_status, discord.Status.dnd),
            activity=activity
        )
        
        self.logger.info(f"Bot logged in as {self.bot.user} ({self.bot.user.id})")
        self.logger.info(f"Connected to {len(self.bot.guilds)} guilds")
        
        await self.bot.tree.sync()
        
        if self.config["auto_config"]["use_autoboosting"]:
            self.logger.info("Starting autoboosting service")
            from fastapi import FastAPI
            from uvicorn import run
            app = FastAPI()
            run(app, host="0.0.0.0", port=self.config["server"]["port"])
        
        if self.config.get("onliner", {}).get("use_onliner"):
            self.logger.info("Starting onliner service")
            asyncio.create_task(onliner())

async def setup(bot):
    await bot.add_cog(ReadyHandler(bot))