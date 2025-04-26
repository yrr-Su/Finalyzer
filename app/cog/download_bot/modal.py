from __future__ import annotations

from pathlib import Path

import discord
from discord.ui import Modal, TextInput

print(Path(__file__).parent.resolve())
PATH_RESOURCE = Path(__file__).parent / '..' / "resource"
AUTHOR_ICON = discord.File(PATH_RESOURCE / "author_icon.jpg")
DEFAULT_PARAMS = {
    '剩餘天數' : '100',
    '已轉換 (%)' : '30',
    '轉換價值' : '75-120',
    '轉換溢價率 (%)' : '3',
    '發債位階' : '70',
    '收盤位階' : '65',
    'CB 收盤價' : '75-120'
}



class DownloadModal(Modal, title="更動參數表"):
    def __init__(self, select) -> None:
        super().__init__()

        if len(select) > 5:
            raise ValueError("最多只能選擇 5 個選項")


        self.param = DEFAULT_PARAMS.copy()
        for key in select:
            _input = TextInput(label=key, default=DEFAULT_PARAMS[key])
            self.add_item(_input)

            self.param[key] = _input.value




    async def on_submit(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="參數表",
            description="以下是輸入的參數：",
            color=discord.Color.blue(),
            timestamp=interaction.created_at
            )

        embed.set_author(
            name="yrr-Su",
            url="https://github.com/yrr-Su",
            icon_url=f"attachment://{AUTHOR_ICON.filename}"
        )

        # for _param in self.params:
        #     embed.add_field(name=_param.label, value=_param.value, inline=True)

        DEFAULT_PARAMS.update(self.param)
        for key, _value in DEFAULT_PARAMS.items():
            embed.add_field(name=key, value=_value, inline=True)

        embed.add_field(name='', value='-'*15, inline=False)
        # embed.add_field(name="剩餘天數", value=self.param.value, inline=False)

        # embed.add_field(name="參數 A", value=self.input_a.value, inline=False)
        # embed.add_field(name="參數 B", value=self.input_b.value or "未輸入", inline=False)

        embed.set_footer(text="莫急莫慌摸摸茶")

        with open("thefew.txt", "w") as f:
            for key, _value in self.param.items():
                f.write(f"{key}: {_value}\n")


        file = discord.File("thefew.txt", filename="thefew.txt")

        await interaction.response.send_message(file=AUTHOR_ICON, embed=embed)
        await interaction.followup.send("拿去補啦:", file=file)
