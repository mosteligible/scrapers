import os
from KijijiScraper.constants import USER_AGENTS
from dotenv import load_dotenv
from pathlib import Path
from random import choice


load_dotenv()


CRAWL_DELAY = 1.5

cur_dir = Path(__file__).parent

HEADERS = {"User-Agent": choice(USER_AGENTS)}

LOG_DIR = cur_dir / "log_store"
LOG_DIR.mkdir(exist_ok=True)

DB_NAME = os.getenv("DB_NAME", "Downloads")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")

TABLE_NAME = os.getenv("TABLE_NAME", "")
