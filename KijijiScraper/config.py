import os
from KijijiScraper.constants import USER_AGENTS
from dotenv import load_dotenv
from pathlib import Path
from random import choice


load_dotenv()


class Configuration:
    def __init__(self):
        self.CRAWL_DELAY = 1.5

        cur_dir = Path(__file__).parent

        self.HEADERS = {"User-Agent": choice(USER_AGENTS)}

        self.LOG_DIR = cur_dir / "log_store"
        self.LOG_DIR.mkdir(exist_ok=True)

        self.DB_NAME = os.getenv("DB_NAME", "Downloads")
        self.DB_USER = os.getenv("DB_USER", "")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        self.DB_HOST = os.getenv("DB_HOST", "")

        self.TABLE_NAME = os.getenv("TABLE_NAME", "")


Config = Configuration()
