from distutils.log import error
import requests
from Handlers.Database import DatabaseCtx
from config import HEADERS, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from log import LOGGER
from pathlib import Path
from urllib.parse import urlparse


def format_string(url: str):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_splitted = path.split("/")
    prefix = "/".join(path_splitted[:-1])
    suffix = path_splitted[-1]
    url_prefix = f"{parsed_url.scheme}://{parsed_url.netloc}{prefix}"
    url_suffix = f"{suffix}?{parsed_url.query}"
    return url_prefix, url_suffix


def flatten_json(ads: dict) -> dict:
    # Validate the schema of json body
    # Then add Null to those keys that haven't been found
    # return flattened dictionary
    
    return {}


def get_database_connection() -> DatabaseCtx:
    db_op = DatabaseCtx(
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME
    )
    return db_op


def collect_response(url: str) -> requests.models.Response:
    retries = 0
    response = None
    while retries < 3:
        try:
            response = requests.get(url, HEADERS, timeout=10)
            response.raise_for_status()
            LOGGER.info(f"<{response.status_code}> - {url}")
            break
        except Exception as e:
            LOGGER.error(f"{e} on {retries+1} tries requesting url:: {url}")
            retries += 1
    return response
