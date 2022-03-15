import threading
from log import create_logger
from utils import get_database_connection, get_page_data, write_to_db


class LongtermRentals(threading.Thread):
    def __init__(
        self,
        url_prefix: str,
        url_suffix: str,
        num_pages: int = None,
        ip_addr: str = "home",
        user_name: str = "self",
    ):
        self._url_prefix = url_prefix
        self._url_suffix = url_suffix
        self.num_pages = num_pages
        self.logger = create_logger(
            logger_name="EXTRACT_LOG", file_name=f"{user_name}@{ip_addr}"
        )
        self.db_ops = get_database_connection()

    def run(self):
        self.current_page_no = 1
        url = f"{self._url_prefix}/page-{current_page_no}/{self._url_suffix}"
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
                target=write_to_db, args=(self.db_op, page_data)
            )
            db_write_thread.start()
            operating_threads.append(db_write_thread)
            current_page_no += 1
            url = f"{self._url_prefix}/page-{current_page_no}/{self._url_suffix}"
