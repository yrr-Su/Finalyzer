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
    DEFAULT_THEFEW_PARAMS = {
        '剩餘天數' : '100',
        '已轉換 (%)' : '30',
        '轉換價值' : '75-120',
        '轉換溢價率 (%)' : '3',
        '發債位階' : '70',
        '收盤位階' : '65',
        'CB 收盤價' : '75-120'
        }
    DEFAULT_THEFEW_PARAMS_DIGIT = {
        '剩餘天數' : 100,
        '已轉換 (%)' : 30,
        '轉換價值' : [75, 120],
        '轉換溢價率 (%)' : 3,
        '發債位階' : 70,
        '收盤位階' : 65,
        'CB 收盤價' : [75, 120]
        }


CONFIG = config()