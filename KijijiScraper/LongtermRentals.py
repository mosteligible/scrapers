import threading


class LongtermRentals(threading.Thread):
    def __init__(self, url_prefix: str, url_suffix: str, num_pages: int = None):
        self.current_page_no = 1
        self.url = f"{url_prefix}/page-{self.current_page_no}/{url_suffix}"
        self.num_pages = num_pages
