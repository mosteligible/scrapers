import logging
import unittest
import requests
from utils import collect_response, format_string, validate_url


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
            ("https://www.kijiji.ca/b-apartments-condos/kingston", "c37l1700276?this=True"),
            (
                "https://www.kijiji.ca/b-apartments-condos/kingston",
                "/c37l1700276?this=True",
            ),
        ]
        for index, url in enumerate(input_urls):
            obtained_output = format_string(url)
            if index % 2 == 0:
                self.assertEqual(test_outputs[index], obtained_output)
            else:
                self.assertNotEqual(test_outputs[index], obtained_output)

    def test_collect_response(self):
        test_urls = [
            "https://httpbin.org/status/200",
            "https://httpbin.org/status/300",
            "https://httpbin.org/status/400",
            "https://httpbin.org/status/500",
            "https://httpbin.org/status/100",
        ]
        exp_type_response = requests.models.Response
        exp_type_none = type(None)
        expected_outputs = [
            exp_type_response,
            exp_type_response,
            exp_type_none,
            exp_type_none,
            exp_type_none,
        ]
        obtained_output = [type(collect_response(url)) for url in test_urls]
        self.assertListEqual(expected_outputs, obtained_output)

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
