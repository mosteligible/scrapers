# -------------------------------------------------------------------
# test_longTermRentals
# -------------------------------------------------------------------
from longTermRentals import get_page_data


def mocked_requests_get(url: str):
    class MockResponse:
        def __init__(self, text: str, status_code: int) -> None:
            self.text = text
            self.status_code = status_code

        def raise_for_status(self):
            if self.status_code == 200:
                return None
            raise ValueError("Did not get 200 status code!")

    if url == "http://www.foo.com":
        return MockResponse(text="pass", status_code=200)
    elif url == "https://www.randomwrongstuff.org":
        return MockResponse(text="fail", status_code=500)

    return MockResponse(text="Not Found", status_code=404)
