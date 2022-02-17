from typing import List
import requests
import mysql.connector
from config import HEADERS, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, TABLE_NAME
from Handlers.Database import DatabaseCtx
from log import LOGGER
from urllib.parse import urlparse
from ScrapeModels import AnAdvertisement


def format_string(url: str):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_splitted = path.split("/")
    prefix = "/".join(path_splitted[:-1])
    suffix = path_splitted[-1]
    url_prefix = f"{parsed_url.scheme}://{parsed_url.netloc}{prefix}"
    url_suffix = f"{suffix}?{parsed_url.query}"
    return url_prefix, url_suffix


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


def write_to_db(db_op: DatabaseCtx, page_data: List) -> None:
    for ad_data in page_data:
        an_advertisement = AnAdvertisement(ad_data)
        if not db_op.is_connected():
            db_op.reconnect(database=DB_NAME)
        try:
            db_op.add_entry(advertisement=an_advertisement.get_json(),
                            table_name=TABLE_NAME)
        except mysql.connector.errors.IntegrityError:
            LOGGER.error(f"adId: {ad_data['adId']} - Duplicate ad encountered")
