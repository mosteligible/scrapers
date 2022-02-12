import requests
from bs4 import BeautifulSoup
from constants import USER_AGENT
import json
from random import choice


class AnAdvertisement(object):
    def __init__(self, datapoint: dict):
        self.__adId = datapoint["adId"]
        self.__data = datapoint["data"]
        self.__collect_information()

    def __collect_information(self):
        nan = float("nan")
        try:
            self.__url = self.__data["url"]
        except:
            self.__url = nan
        try:
            self.__rent = self.__data["rent"]["amount"] / 100
        except:
            self.__rent = nan
        try:
            self.__description = self.__data["description"]
        except:
            self.__description = nan
        try:
            self.__latitude = self.__data["location"]["latitude"]
        except:
            self.__latitude = nan
        try:
            self.__longitude = self.__data["location"]["longitude"]
        except:
            self.__longitude = nan
        try:
            self.__address = self.__data["location"]["mapAddress"]
        except:
            self.__address = nan
        try:
            self.__province = self.__data["location"]["province"]
        except:
            self.__province = nan
        try:
            self.__utilities = self.__data["utility"]
        except:
            self.__utilities = nan
        try:
            self.__bedrooms = self.__data["Bedrooms"]
        except:
            self.__bedrooms = nan
        try:
            self.__bathrooms = self.__data["Bathrooms"]
        except:
            self.__bathrooms = nan
        try:
            self.__furnished = self.__data["Furnished"]
        except:
            self.__furnished = nan
        try:
            self.__rentedBy = self.__data["For Rent By"]
        except:
            self.__rentedBy = nan
        try:
            self.__petFriendly = self.__data["Pet Friendly"]
        except:
            self.__petFriendly = nan
        try:
            self.__laundry = self.__data["laundry"]
        except:
            self.__laundry = nan
        try:
            self.__adAttributes = self.__data["adAttributes"]
        except:
            self.__adAttributes = nan

    def __str__(self):
        return (
            f"Advertisement with id {self.__adId} costs ${self.__rent} at {self.__address}"
        )

    def get_json(cls):
        return cls.__dict__

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

        self.__response = requests.get(self.__url, headers=USER_AGENT)
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
