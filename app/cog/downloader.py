from __future__ import annotations

import discord
from discord.ext import commands
from discord.ui import View, Button

from app.cog.download_bot.selection import DownloadSelectionView


class WorkView(View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

        upload_btn = Button(label="Upload", style=discord.ButtonStyle.primary)
        download_btn = Button(label="Download", style=discord.ButtonStyle.success)

        upload_btn.callback = self.upload_callback
        download_btn.callback = self.download_callback

        self.add_item(upload_btn)
        self.add_item(download_btn)

    async def upload_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("請上傳你的檔案。", ephemeral=False)

    async def download_callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(
                view=DownloadSelectionView()
                )
        except Exception as e:
            await interaction.response.send_message(f"發生錯誤，請稍後再試。\n{e}")

class Processor(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="work")
    async def work(self, ctx) -> None:
        view = WorkView()
        await ctx.send("請選擇你要的動作：", view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Processor(bot))


