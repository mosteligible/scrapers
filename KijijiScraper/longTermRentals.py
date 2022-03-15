import KijijiScraper.utils as utils
import time
from bs4 import BeautifulSoup
from KijijiScraper.config import Config
from KijijiScraper.log import LOGGER
from urllib.parse import urlparse


def get_page_data(url: str) -> list:
    response = utils.collect_response(url)
    soup = BeautifulSoup(response.content, features="lxml")
    ad_data = []
    regular_postings = soup.find_all("div", {"class": "search-item regular-ad"})
    parsed_url = urlparse(url)
    for a_posting in regular_postings:
        time.sleep(Config.CRAWL_DELAY)
        href = a_posting.find("a", {"class": "title"}).get("href")
        new_posting = parsed_url.scheme + "://" + parsed_url.netloc + href
        an_ad = {}
        data_returned = utils.advertisement_details(new_posting)
        if data_returned == "data could not be read!":
            continue
        else:
            an_ad["adId"], an_ad["data"] = data_returned
        ad_data.append(an_ad)
    LOGGER.info(f"Completed from {url}")
    return ad_data
