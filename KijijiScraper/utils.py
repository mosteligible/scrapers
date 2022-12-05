from bs4 import BeautifulSoup
from typing import List
import requests
import mysql.connector
from KijijiScraper.config import Config
from KijijiScraper.Handlers import DatabaseCtx
from KijijiScraper.log import LOGGER, LOG_DB_ADD_ENTRY
from urllib.parse import urlparse
from KijijiScraper.ScrapeModels import AnAdvertisement, KijijiScraper_AnAdvertisement


def advertisement_details(url: str) -> dict:
    """
    This function takes in the link to an advertisement and returns the content
    of the page as JSON.
    """
    response = collect_response(url)
    if response is not None:
        soup = BeautifulSoup(response, "lxml")
        a_scraped_ad = KijijiScraper_AnAdvertisement(soup)
    else:
        LOGGER.error("Error during reading page!")
        return "data could not be read!"

    advertisementData = {}
    adId = a_scraped_ad.get_adId()
    advertisementData["url"] = url
    advertisementData["adType"] = a_scraped_ad.get_adType()
    advertisementData["rent"] = a_scraped_ad.get_rent()
    advertisementData["description"] = a_scraped_ad.get_description()
    advertisementData["location"] = a_scraped_ad.get_location()
    advertisementData["adAttributes"] = a_scraped_ad.get_adAttributes()
    return adId, advertisementData


def format_url(url: str):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_splitted = path.split("/")
    prefix = "/".join(path_splitted[:-1])
    suffix = path_splitted[-1]
    url_prefix = f"{parsed_url.scheme}://{parsed_url.netloc}{prefix}"
    if parsed_url.query != "":
        url_suffix = f"{suffix}?{parsed_url.query}"
    else:
        url_suffix = f"{suffix}"
    return url_prefix, url_suffix


def get_database_connection() -> DatabaseCtx:
    db_op = DatabaseCtx(
        username=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        database=Config.DB_NAME,
    )
    return db_op


def collect_response(url: str) -> str:
    retries = 0
    response = ""
    while retries < 3:
        try:
            response = requests.get(url, Config.HEADERS, timeout=3)
            response.raise_for_status()
            LOGGER.info(f"<{response.status_code}> - {url}")
            break
        except Exception as e:
            LOGGER.error(f"{e} on {retries+1} tries requesting url:: {url}")
            retries += 1
    return response if response == "" else response.text


def validate_url(url: str) -> bool:
    LOGGER.info(f"Validating url for provided url: {url}")
    parsed_url = urlparse(url)
    if parsed_url.netloc == "" or parsed_url.scheme == "" or "://" not in url:
        LOGGER.error("URL validation Failed, URL is invalid!")
    elif "kijiji.ca" not in parsed_url.netloc.lower():
        LOGGER.error(f"URL validation Failed, Passed url should be kijiji's valid url!")
    elif "kijiji.ca" in parsed_url.netloc.lower() and len(parsed_url.path.split("/")) == 4:
        return True
    return False


def write_to_db(db_op: DatabaseCtx, page_data: List) -> None:
    for ad_data in page_data:
        an_advertisement = AnAdvertisement(ad_data)
        if not db_op.is_connected():
            db_op.reconnect(database=Config.DB_NAME)
        try:
            db_op.add_entry(
                advertisement=an_advertisement.get_json(), table_name=Config.TABLE_NAME
            )
        except mysql.connector.errors.IntegrityError:
            LOG_DB_ADD_ENTRY.error(f"adId: {ad_data['adId']} - Duplicate ad encountered")
