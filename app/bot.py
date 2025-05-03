
from __future__ import annotations

from pathlib import Path

import discord
from discord.ext import commands

from config.setting import CONFIG

__all__ = [
    "bot_server"
]



intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
# intents.message_content = True
# client = discord.Client(intents = intents)

PATH_COG = Path('cog')


@bot.command()
async def load(ctx, extension) -> None:
    await bot.load_extension(f"app.cog.{extension}")
    # await bot.load_extension(f"app.cog.{extension}")
    await ctx.send(f"Loaded {extension} done.")


@bot.command()
async def unload(ctx, extension) -> None:
    await bot.unload_extension(f"app.cog..{extension}")
    await ctx.send(f"UnLoaded {extension} done.")


@bot.command()
async def reload(ctx, extension) -> None:
    await bot.reload_extension(f"app.cog.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")

@bot.command()
async def reload_all(ctx) -> None:
    for filename in PATH_COG.glob("*.py"):
        await bot.reload_extension(f"cog.{filename.stem}")
    await ctx.send("Reload all done.")



async def load_extensions() -> None:
    await bot.load_extension("app.cog.downloader")
    # await bot.load_extension("uploader")


@bot.event
async def on_command_error(ctx, error) -> None:
    print(f"錯誤內容：{error}")
    await ctx.send(f"執行指令時發生錯誤：{str(error)}")

@bot.event
async def on_application_command_error(ctx, error) -> None:
    print(f"應用指令錯誤：{error}")




async def bot_server() -> None:
    async with bot:
        await load_extensions()

        print("Bot is running...")
        await bot.start(CONFIG.DISCORD_BOT)



