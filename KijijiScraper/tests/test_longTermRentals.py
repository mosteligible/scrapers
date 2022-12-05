import unittest
from unittest.mock import patch

from longTermRentals import get_page_data
from tests.test_data import mocked_requests_get


class TestLongTermRentals(unittest.TestCase):
    def test_advertisement_details(self):
        pages = [
            "http://www.foo.com",
            "https://www.bar.foo",
            "https://www.randomwrongstuff.org",
        ]
