import os
from KijijiScraper.constants import USER_AGENTS, TIMESTAMP_FORMAT
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from random import choice


load_dotenv()


def get_workdir():
    now = datetime.now().strftime(TIMESTAMP_FORMAT)
    return LONGTERM_JSON_PATH


CRAWL_DELAY = 1.5

cur_dir = Path(__file__).parent

HEADERS = {"User-Agent": choice(USER_AGENTS)}

LOG_DIR = cur_dir / "log_store"
LOG_DIR.mkdir(exist_ok=True)
LONGTERM_JSON_PATH = cur_dir / "longterm_json"
LONGTERM_JSON_PATH.mkdir(exist_ok=True)
LONGTERM_STRUCTURED = cur_dir / "longterm_structures"
LONGTERM_STRUCTURED.mkdir(exist_ok=True)

DB_NAME = os.getenv("DB_NAME", "Downloads")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")

TABLE_NAME = os.getenv("TABLE_NAME", "")
