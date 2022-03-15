import threading
from .config import Config
from .log import create_logger
from .utils import (
    format_url,
    get_database_connection,
    get_page_data,
    write_to_db,
    format_url,
)


class LongtermRentals(threading.Thread):
    def __init__(
        self,
        url: str,
        num_pages: int = None,
        ip_addr: str = "home",
        user_name: str = "self",
    ):
        super(LongtermRentals, self).__init__()
        self._url_prefix, self._url_suffix = format_url(url)
        self.num_pages = num_pages
        self.logger = create_logger(
            logger_name="EXTRACT_LOG", file_name=Config.LOG_DIR / f"{user_name}@{ip_addr}"
        )
        self.db_ops = get_database_connection()

    def run(self):
        self.current_page_no = 1
        url = f"{self._url_prefix}/page-{self.current_page_no}/{self._url_suffix}"
        previous_page_id = []
        operating_threads = []
        if self.num_pages is None:
            self.num_pages = float("inf")
        while self.current_page_no <= self.num_pages:
            page_data = get_page_data(url)

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
            url = f"{self._url_prefix}/page-{self.current_page_no}/{self._url_suffix}"
