import logging
import unittest
import requests
from unittest import mock
from unittest.mock import patch

from tests.test_data import mocked_requests_get

from config import Config
from utils import collect_response, format_url, validate_url


logging.disable(logging.CRITICAL)


class TestUtils(unittest.TestCase):
    def test_formatstring(self):
        input_urls = [
            "https://www.kijiji.ca/b-apartments-condos/mississauga-peel-region/c37l1700276",
            "https://www.kijiji.ca/b-apartments-condos/ottawa/c37l1700276",
            "https://www.kijiji.ca/b-apartments-condos/kingston/c37l1700276?this=True",
            "https://www.kijiji.ca/b-apartments-condos/kingston/c37l1700276?this=True",
        ]
        test_outputs = [
            (
                "https://www.kijiji.ca/b-apartments-condos/mississauga-peel-region",
                "c37l1700276",
            ),
            ("https://www.kijiji.ca/b-apartments-condos/ottawa/", "c37l1700276"),
            (
                "https://www.kijiji.ca/b-apartments-condos/kingston",
                "c37l1700276?this=True",
            ),
            (
                "https://www.kijiji.ca/b-apartments-condos/kingston",
                "/c37l1700276?this=True",
            ),
        ]
        for index, url in enumerate(input_urls):
            obtained_output = format_url(url)
            if index % 2 == 0:
                self.assertEqual(test_outputs[index], obtained_output)
            else:
                self.assertNotEqual(test_outputs[index], obtained_output)

    def test_validate_url(self):
        input_urls = [
            "https://www.kijiji.ca/b-apartments-condos/mississauga-peel-region/c37l1700276",
            "https://httpbin.org/status/200",
            "www.kijiji.ca/b-apartments-condos/mississauga-peel-region/c37l1700276",
            "https:/www.kijiji.ca/b-apartments-condos/mississauga-peel-region/c37l1700276",
        ]
        expected_outputs = [True, False, False, False]
        obtained_outputs = [validate_url(url) for url in input_urls]
        self.assertListEqual(expected_outputs, obtained_outputs)

    @patch("KijijiScraper.utils.requests.get", side_effect=mocked_requests_get)
    def test_advertisement_details(self, mock_get):
        pages = {
            "http://www.foo.com": "pass",
            "https://www.bar.foo": "fail",
            "https://www.randomwrongstuff.org": "Not Found",
        }
        for url in pages:
            response_body = collect_response(url=url)
            print("mock_get.call", mock.call(url), f"response_body: <{response_body}>")
            self.assertEqual(response_body, pages[url])


if __name__ == "__main__":
    unittest.main()
