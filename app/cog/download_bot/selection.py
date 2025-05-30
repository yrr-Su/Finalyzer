from __future__ import annotations

import discord
from discord.ui import View, Select

from app.cog.download_bot.modal import DownloadModal

class DownloadSelection(Select):
    def __init__(self) -> None:
        options = [
            discord.SelectOption(label="不更改參數", description="請不要點選其他選項"),
            discord.SelectOption(label="剩餘天數", description="default: 100"),
            discord.SelectOption(label="已轉換 (%)", description="default: 30"),
            discord.SelectOption(label="轉換價值", description="default: 75-120"),
            discord.SelectOption(label="轉換溢價率 (%)", description="default: 3"),
            discord.SelectOption(label="發債位階", description="default: 70"),
            discord.SelectOption(label="收盤位階", description="default: 65"),
            discord.SelectOption(label="CB 收盤價", description="default: 75-120"),
        ]

        super().__init__(
            placeholder="選擇改寫項目",
            min_values=0,
            max_values=5,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(DownloadModal(self.values))
        except Exception as e:
            await interaction.response.send_message(
                f"發生錯誤：{e}"
            )


class DownloadSelectionView(View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(DownloadSelection())

