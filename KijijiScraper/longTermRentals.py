import KijijiScraper.utils as utils
import KijijiScraper.ScrapeModels as ScrapeModels
import time
import threading
from bs4 import BeautifulSoup
from KijijiScraper.config import CRAWL_DELAY
from KijijiScraper.log import LOGGER
from urllib.parse import urlparse


def advertisement_details(url: str) -> dict:
    """
    This function takes in the link to an advertisement and returns the content
    of the page as JSON.
    """
    response = utils.collect_response(url)
    if response is not None:
        soup = BeautifulSoup(response.content, "lxml")
        a_scraped_ad = ScrapeModels.KijijiScraper_AnAdvertisement(soup)
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
    response = utils.collect_response(url)
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
    LOGGER.info(f"Completed from {url}")
    return ad_data


def longterm_main(url_prefix: str, url_suffix: str, num_pages: int = None):
    # TODO: Validate URL
    LOGGER.info("initiating Longterm Scrapes")
    db_op = utils.get_database_connection()
    # LONG TERM RENTALS
    current_page_no = 1
    url = f"{url_prefix}/page-{current_page_no}/{url_suffix}"

    previous_page_id = []
    operating_threads = []
    if num_pages is None:
        num_pages = float("inf")
    while current_page_no <= num_pages:
        page_data = get_page_data(url)

        if page_data == "data could not be read!":
            continue

        current_page_ids = [i["adId"] for i in page_data]
        if previous_page_id == current_page_ids:
            break

        previous_page_id = current_page_ids.copy()

        db_write_thread = threading.Thread(
            target=utils.write_to_db, args=(db_op, page_data)
        )
        db_write_thread.start()
        operating_threads.append(db_write_thread)
        current_page_no += 1
        url = f"{url_prefix}/page-{current_page_no}/{url_suffix}"
