from __future__ import annotations

import asyncio

import discord
from discord.ui import Modal, TextInput

from config.setting import CONFIG
from FinCrawler.builder import CrawlerBuilder


class DownloadModal(Modal, title="更動參數表"):
    def __init__(self, select) -> None:
        super().__init__(timeout=300)

        self.status = 'choose'
        self.update_param, self.textinput = {}, {}
        self.default_param = CONFIG.DEFAULT_THEFEW_PARAMS.copy()
        self.author_icon = discord.File(
            CONFIG.PATH_APP_RESOURCE / "author_icon.jpg")

        if ('不更改參數' in select) & (len(select) == 1):
            self.status = 'no_change'
            self.add_item(TextInput(
                label="不更改參數",
                default="請不要點選其他選項",
                ))
        else:
            raise ValueError("請不要點選 '不更改參數' 或是 僅點選 '不更改參數'")

        if len(select) > 5:
            raise ValueError("最多只能選擇 5 個選項")

        if self.status == 'choose':
            for key in select:
                self.textinput[key] = TextInput(
                            label=key,
                            placeholder=CONFIG.DEFAULT_THEFEW_PARAMS[key]
                            )
                self.add_item(self.textinput[key])


    async def on_submit(self, interaction: discord.Interaction):

        for _key, _textinput in self.textinput.items():
            self.update_param[_key] = _textinput.value


        embed = discord.Embed(
            title="參數表",
            description="以下是輸入的參數：",
            color=discord.Color.blue(),
            timestamp=interaction.created_at
            )

        embed.set_author(
            name="yrr-Su",
            url="https://github.com/yrr-Su",
            # icon_url=f"attachment://{self.author_icon.filename}"
        )

        self.default_param.update(self.update_param)
        for _key, _value in self.default_param.items():
            embed.add_field(name=_key, value=_value, inline=True)

        embed.add_field(name='', value='-'*15, inline=False)
        embed.set_footer(text="莫急莫慌摸摸茶")
        await interaction.response.send_message(embed=embed)

        async def _build_and_send() -> None:
            builder = CrawlerBuilder(rules=self.update_param,
                                     output=CONFIG.OUTPUT)
            path_output_file = builder.build()

            file = discord.File(path_output_file,
                                filename=path_output_file.name)
            await interaction.followup.send("拿去補啦:", file=file)

        asyncio.create_task(_build_and_send())
