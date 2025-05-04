import asyncio
import discord
from discord.ext import commands
from utils.logger import setup_logger
from utils.embed_builder import EmbedBuilder  # Thêm dòng này
import json
import time
import os
from colorama import Fore, Style

logger = setup_logger()

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file config tại {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Định dạng JSON không hợp lệ trong {config_path}")

async def load_cogs(bot):
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f"Loaded cog: {filename[:-3]}")

async def main():
    config = load_config()
    intents = discord.Intents.all()
    bot = commands.Bot(
        command_prefix=config["bot"]["prefix"],
        intents=intents,
        case_insensitive=True
    )
    bot.embed_builder = EmbedBuilder()

    start_time = time.time()
    logo = f"""
{Fore.CYAN}══════════════════════════════════════════════════════{Style.RESET_ALL}

{Fore.MAGENTA}███████╗███████╗ █████╗     ███████╗████████╗ ██████╗ ██████╗ ███████╗    
██╔════╝██╔════╝██╔══██╗    ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝    
███████╗█████╗  ███████║    ███████╗   ██║   ██║   ██║██████╔╝█████╗      
╚════██║██╔══╝  ██╔══██║    ╚════██║   ██║   ██║   ██║██╔══██╗██╔══╝      
███████║███████╗██║  ██║    ███████║   ██║   ╚██████╔╝██║  ██║███████╗    
╚══════╝╚══════╝╚═╝  ╚═╝    ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝    {Style.RESET_ALL}
                                                                          

{Fore.CYAN}══════════════════════════════════════════════════════{Style.RESET_ALL}
{Fore.GREEN}Starting Discord Boost Bot...{Style.RESET_ALL}
    """
    print(logo)

    await load_cogs(bot)
    
    try:
        await bot.start(config["bot"]["token"])
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
    
    logger.info(f"Bot started in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    discord.utils.setup_logging()
    asyncio.run(main())