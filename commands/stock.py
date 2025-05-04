import discord
import os
from utils.embed_builder import EmbedBuilder
from config.config import load_config

config = load_config()
embed_builder = EmbedBuilder()

async def add_stock(ctx, month: int, tokens: str):
    if month not in [1, 3]:
        await ctx.send(embed=embed_builder.error("Invalid month. Use 1 or 3"))
        return
    
    filename = f"data/{month}m.txt"
    tokens_list = tokens.split("\n")
    
    with open(filename, "a") as file:
        for token in tokens_list:
            if token.strip():
                file.write(f"{token.strip()}\n")
    
    await ctx.send(embed=embed_builder.success(
        f"Added {len(tokens_list)} tokens to {month}m stock",
        "Stock Added"
    ))

async def view_stock(ctx):
    stock_info = ""
    for month in [1, 3]:
        filename = f"data/{month}m.txt"
        try:
            with open(filename, "r") as file:
                tokens = file.read().splitlines()
                stock_info += f"**{month} Month Stock:** {len(tokens)} tokens\n"
        except FileNotFoundError:
            stock_info += f"**{month} Month Stock:** 0 tokens\n"
    
    await ctx.send(embed=embed_builder.success(stock_info, "Stock Status"))

async def remove_stock(ctx, month: int, quantity: int):
    if month not in [1, 3]:
        await ctx.send(embed=embed_builder.error("Invalid month. Use 1 or 3"))
        return
    
    filename = f"data/{month}m.txt"
    try:
        with open(filename, "r") as file:
            tokens = file.read().splitlines()
        
        if len(tokens) < quantity:
            await ctx.send(embed=embed_builder.error(f"Not enough tokens in {month}m stock"))
            return
        
        tokens = tokens[quantity:]
        with open(filename, "w") as file:
            for token in tokens:
                file.write(f"{token}\n")
        
        await ctx.send(embed=embed_builder.success(
            f"Removed {quantity} tokens from {month}m stock",
            "Stock Removed"
        ))
    except FileNotFoundError:
        await ctx.send(embed=embed_builder.error(f"No {month}m stock found"))