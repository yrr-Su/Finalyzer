from __future__ import annotations

import os
from importlib import resources
from pathlib import Path

from dotenv import load_dotenv


class config:

    if load_dotenv(Path(str(resources.files('local').joinpath('.env.local')))):
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

CONFIG = config()