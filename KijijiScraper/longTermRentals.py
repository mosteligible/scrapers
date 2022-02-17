import time
import threading
from bs4 import BeautifulSoup
from config import CRAWL_DELAY, DB_NAME, LONGTERM_JSON_PATH, TABLE_NAME, get_workdir
from data_models import AnAdvertisement, KijijiScraper_AnAdvertisement
from log import LOGGER
from urllib.parse import urlparse
from utils import collect_response, get_database_connection


WORKDIR = get_workdir()


def advertisement_details(url: str) -> dict:
    """
    This function takes in the link to an advertisement and returns the content
    of the page as JSON.
    """
    response = collect_response(url)
    if response.status_code >= 200 and response.status_code < 400:
        soup = BeautifulSoup(response.content, "lxml")
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


def get_page_data(url: str) -> list:
    response = collect_response(url)
    soup = BeautifulSoup(response.content, features="lxml")
    ad_data = []
    regular_postings = soup.find_all("div", {"class": "search-item regular-ad"})
    parsed_url = urlparse(url)
    for a_posting in regular_postings:
        time.sleep(CRAWL_DELAY)
        href = a_posting.find("a", {"class": "title"}).get("href")
        new_posting = parsed_url.scheme + "://" + parsed_url.netloc + href
        an_ad = {}
        data_returned = advertisement_details(new_posting)
        if data_returned == "data could not be read!":
            continue
        else:
            an_ad["adId"], an_ad["data"] = data_returned
        ad_data.append(an_ad)
    LOGGER.info(f"Collected from {url}")
    return ad_data


def are_two_equal(a, b):
    return a == b


def longterm_main(url_prefix: str, url_suffix: str):
    # select page number 1
    LOGGER.info("initiating Longterm Scrapes")
    db_op = get_database_connection()
    current_page_no = 1
    # LONG TERM RENTALS
    url = f"{url_prefix}/page-{current_page_no}/{url_suffix}"

    flag = True
    previous_page_id = []
    while flag:
        # LONG TERM RENTALS
        url = f"{url_prefix}/page-{current_page_no}/{url_suffix}"

        LOGGER.info(f"COLLECTING FROM: {url}")
        page_data = get_page_data(url)

        if page_data == "data could not be read!":
            continue

        current_page_ids = [i["adId"] for i in page_data]
        if are_two_equal(previous_page_id, current_page_ids):
            break

        previous_page_id = current_page_ids.copy()

        for ad_data in page_data:
            an_advertisement = AnAdvertisement(ad_data)
            if not db_op.is_connected():
                db_op.reconnect(database=DB_NAME)
            db_op.add_entry(advertisement=an_advertisement.get_json(),
                            table_name=TABLE_NAME)
        
        current_page_no += 1
