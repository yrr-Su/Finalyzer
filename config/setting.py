from __future__ import annotations

import os
from importlib import resources
from pathlib import Path

from dotenv import load_dotenv


class config:

    if load_dotenv(Path(str(resources.files('storage').joinpath('.env.local')))):
        pass
    else:
        raise FileNotFoundError("No .env.local file found.")

    OUTPUT: Path = Path(os.getenv('OUTPUT', 'output'))

    PATH_MAIN_RESOURCE: Path = Path(
        str(resources.files('FinCrawler').joinpath('resources'))
        )
    PATH_APP_RESOURCE: Path = Path(
        str(resources.files('app').joinpath('resources'))
        )

    DISCORD_BOT: str = os.getenv('DISCORD_BOT', '')

    GOOGLE_ACCOUNT: str = os.getenv('GOOGLE_ACCOUNT', '')
    GOOGLE_PASSWORD: str = os.getenv('GOOGLE_PASSWORD', '')

    THEFEW_PARAMS = {
        "PARAMS_STR": {
            '剩餘天數' : '100',
            '已轉換 (%)' : '30',
            '轉換價值' : '75-120',
            '轉換溢價率 (%)' : '3',
            '發債位階' : '70',
            '收盤位階' : '65',
            'CB 收盤價' : '75-120'
            },

        "PARAMS_DIGIT": {
            '剩餘天數' : 100,
            '已轉換 (%)' : 30,
            '轉換價值' : [75, 120],
            '轉換溢價率 (%)' : 3,
            '發債位階' : 70,
            '收盤位階' : 65,
            'CB 收盤價' : [75, 120]
            },

        "PARAMS_SUFFIX": {
            '剩餘天數': 'Days',
            '已轉換 (%)': 'Conv',
            '轉換價值': 'Val',
            '轉換溢價率 (%)': 'Prem',
            '發債位階': 'Issue',
            '收盤位階': 'Close',
            'CB 收盤價': 'CB'
            }
    }



CONFIG = config()
