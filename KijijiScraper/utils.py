import requests
from bs4 import BeautifulSoup
import json
from random import choice


class SegmentData(object):
    def __init__(self, datapoint: dict):
        self.__datapoint = datapoint
        self.__adId = self.__datapoint["adId"]
        self.__data = self.__datapoint["data"]
        self.nan = float("nan")
        self.__collect_information()

    def __collect_information(self):
        try:
            self.__url = self.__data["url"]
        except:
            self.__url = self.nan
        try:
            self.__rent = self.__data["rent"]["amount"] / 100
        except:
            self.__rent = self.nan
        try:
            self.__description = self.__data["description"]
        except:
            self.__description = self.nan
        try:
            self.__latitude = self.__data["location"]["latitude"]
        except:
            self.__latitude = self.nan
        try:
            self.__longitude = self.__data["location"]["longitude"]
        except:
            self.__longitude = self.nan
        try:
            self.__address = self.__data["location"]["mapAddress"]
        except:
            self.__address = self.nan
        try:
            self.__province = self.__data["location"]["province"]
        except:
            self.__province = self.nan
        try:
            self.__utilities = self.__data["utility"]
        except:
            self.__utilities = self.nan
        try:
            self.__bedrooms = self.__data["Bedrooms"]
        except:
            self.__bedrooms = self.nan
        try:
            self.__bathrooms = self.__data["Bathrooms"]
        except:
            self.__bathrooms = self.nan
        try:
            self.__furnished = self.__data["Furnished"]
        except:
            self.__furnished = self.nan
        try:
            self.__rentedBy = self.__data["For Rent By"]
        except:
            self.__rentedBy = self.nan
        try:
            self.__petFriendly = self.__data["Pet Friendly"]
        except:
            self.__petFriendly = self.nan
        try:
            self.__laundry = self.__data["laundry"]
        except:
            self.__laundry = self.nan
        try:
            self.__adAttributes = self.__data["adAttributes"]
        except:
            self.__adAttributes = self.nan

    def __str__(self):
        return (
            f"Advertisement with id {self.__adId} costs ${self.__rent} at {self.__address}"
        )

    def get_adid(self):
        return self.__adId

    def get_url(self):
        return self.__url

    def is_utilities_included(self):
        return self.__utilities

    def is_pet_friendly(self):
        return self.__petFriendly

    def get_rent(self):
        return self.__rent

    def get_description(self):
        return self.__description

    def get_latitude(self):
        return self.__latitude

    def get_longiutde(self):
        return self.__longitude

    def get_address(self):
        return self.__address

    def get_province(self):
        return self.__province

    def get_numBedrooms(self):
        return self.__bedrooms

    def get_numBathrooms(self):
        return self.__bathrooms

    def isFurnished(self):
        return self.__furnished

    def who_is_renting(self):
        return self.__rentedBy

    def get_laundry(self):
        return self.__laundry

    def get_adAttributes(self):
        return self.__adAttributes


class KijijiScraper_AnAdvertisement(object):
    def __init__(self, url: str):  # , proxy):
        self.__url = url

        self.__user_agents = [
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
            },
            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
            },
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"
            },
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"
            },
            {
                "User-Agent": "Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1"
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
            },
            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36"
            },
            {
                "User-Agent": "Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3"
            },
            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36"
            },
            {
                "User-Agent": "Mozilla/5.0 (iPod; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/85.0.4183.92 Mobile/15E148 Safari/604.1"
            },
            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36"
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
            },
            {
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
            },
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"
            },
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
            },
        ]

        # self.__proxy = proxy

        self.__response = requests.get(
            self.__url,
            headers=choice(self.__user_agents),
            # proxies={'http':proxy, 'https':proxy}
        )
        self.__data = (
            BeautifulSoup(self.__response.content, "lxml")
            .find("div", {"id": "FesLoader"})
            .contents[1]
        )
        self.__data = json.loads(str(self.__data)[31 + 14 : -10])
        self.__nan = float("nan")

    def get_adId(self):
        try:
            return self.__data["config"]["VIP"]["adId"]
        except:
            return None

    def get_adType(self):
        try:
            return self.__data["config"]["VIP"]["adType"]
        except:
            return self.__nan

    def get_rent(self):
        try:
            return self.__data["config"]["VIP"]["price"]
        except:
            return self.__nan

    def get_description(self):
        try:
            return self.__data["config"]["VIP"]["description"]
        except:
            return self.__nan

    def get_location(self):
        try:
            return self.__data["config"]["VIP"]["adLocation"]
        except:
            return self.__nan

    def get_adAttributes(self):
        try:
            return self.__data["config"]["VIP"]["adAttributes"]
        except:
            return self.__nan
