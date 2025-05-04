import discord
import asyncio
from utils.booster import Booster
from utils.embed_builder import EmbedBuilder
from config.config import load_config
from commands.boost import getinviteCode, checkInvite, getStock, remove

config = load_config()
embed_builder = EmbedBuilder()

auto_boost_task = None

async def start_auto_boost(ctx):
    global auto_boost_task
    if auto_boost_task is not None:
        await ctx.send(embed=embed_builder.error("Auto-boosting is already running"))
        return
    
    async def auto_boost_loop():
        while True:
            for month in [1, 3]:
                filename = f"data/{month}m.txt"
                tokens = getStock(filename)
                if not tokens:
                    continue
                
                invite = config["auto_config"].get("default_invite", "")
                if not invite:
                    continue
                
                invite_code = getinviteCode(invite)
                guild_id = checkInvite(invite_code)
                if not guild_id:
                    continue
                
                booster = Booster()
                token = tokens.pop(0)
                remove(token, filename)
                
                status = booster.thread(invite_code, [token], guild_id)
                if status["success"]:
                    await ctx.send(embed=embed_builder.success(
                        f"Auto-boosted server .gg/{invite_code} with 2x {month}m boosts",
                        "Auto Boost"
                    ))
                else:
                    await ctx.send(embed=embed_builder.error(
                        f"Auto-boost failed for .gg/{invite_code}",
                        "Auto Boost Failed"
                    ))
                
                await asyncio.sleep(config["advanced"]["refresh_interval"])
    
    auto_boost_task = asyncio.create_task(auto_boost_loop())
    await ctx.send(embed=embed_builder.success("Auto-boosting started", "Auto Boost"))

async def stop_auto_boost(ctx):
    global auto_boost_task
    if auto_boost_task is None:
        await ctx.send(embed=embed_builder.error("Auto-boosting is not running"))
        return
    
    auto_boost_task.cancel()
    auto_boost_task = None
    await ctx.send(embed=embed_builder.success("Auto-boosting stopped", "Auto Boost"))

async def auto_boost_status(ctx):
    status = "Running" if auto_boost_task is not None else "Stopped"
    await ctx.send(embed=embed_builder.info(f"Auto-boosting status: {status}", "Auto Boost Status"))