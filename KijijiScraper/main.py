import argparse

from KijijiScraper.log import LOGGER
from .longTermRentals import longterm_main
from .utils import format_string, validate_url


def run(url: str, num_pages: int):
    if not validate_url(url=url):
        return None
    url_prefix, url_suffix = format_string(url)
    longterm_main(url_prefix, url_suffix, num_pages=num_pages)
    LOGGER.info(f"Complete for url: {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Tool for downloading ads information from kijiji",
        description="Fetches advertisement details from kijiji for category of url supplied",
    )
    parser.add_argument(
        "--url",
        type=str,
        dest="url",
        required=True,
        help="First page of the advertisements being extracted. If Real-estate \
            data is being searched, it should be url to first page of search.",
    )
    parser.add_argument(
        "--num-pg",
        type=int,
        dest="num_pages",
        help="Specifies the number of pages of advertisements to download.",
    )

    arguments = parser.parse_args()
    url = arguments.url
    num_pages = arguments.num_pages
    run(url)
