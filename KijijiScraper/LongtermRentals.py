import threading
import time
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urlparse

from .config import Config
from .log import create_logger
from .utils import (
    advertisement_details,
    collect_response,
    format_url,
    get_database_connection,
    write_to_db,
    format_url,
)


class LongtermRentals(threading.Thread):
    _lock = {}

    def __init__(
        self,
        url: str,
        num_pages: int = None,
        ip_addr: str = "home",
        user_name: str = "self",
    ):
        self._url_prefix, self._url_suffix = format_url(url)
        self.num_pages = num_pages
        self.logger = create_logger(
            logger_name="EXTRACT_LOG",
            file_name=Config.LOG_DIR / f"{user_name}@{ip_addr}",
        )
        self.domain = urlparse(url=url).netloc
        self._lock[self.domain] = threading.Lock()
        self.db_ops = get_database_connection()

    # Add redis to check if a given page data has been already collected
    def get_page_data(self, url: str) -> List:
        domain_lock = self._lock[self.domain]
        with domain_lock:
            response = collect_response(url)
        soup = BeautifulSoup(response.content, features="lxml")
        ad_data = []
        regular_postings = soup.find_all("div", {"class": "search-item regular-ad"})
        parsed_url = urlparse(url)
        for a_posting in regular_postings:
            time.sleep(Config.CRAWL_DELAY)
            href = a_posting.find("a", {"class": "title"}).get("href")
            new_posting = parsed_url.scheme + "://" + parsed_url.netloc + href
            an_ad = {}
            data_returned = advertisement_details(new_posting)
            if data_returned == "data could not be read!":
                continue
            else:
                an_ad["adId"], an_ad["data"] = data_returned
            ad_data.append(an_ad)
        self.logger.info(f"Completed from {url}")
        return ad_data

    def run(self) -> None:
        self.current_page_no = 1
        previous_page_id = []
        operating_threads = []
        if self.num_pages is None:
            self.num_pages = float("inf")
        while self.current_page_no <= self.num_pages:
            url = f"{self._url_prefix}/page-{self.current_page_no}/{self._url_suffix}"
            page_data = self.get_page_data(url)

            if page_data == "data could not be read!":
                continue

            current_page_ids = [i["adId"] for i in page_data]
            if previous_page_id == current_page_ids:
                break

            previous_page_id = current_page_ids.copy()

            db_write_thread = threading.Thread(
                target=write_to_db, args=(self.db_op, page_data)
            )
            db_write_thread.start()
            operating_threads.append(db_write_thread)
            self.current_page_no += 1
