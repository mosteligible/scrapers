import json
from bs4 import BeautifulSoup
from constants import COLUMN_NAMES, USER_AGENT


class AnAdvertisement(object):
    def __init__(self, datapoint: dict):
        self.adId = datapoint["adId"]
        self.__collect_information(datapoint["data"])

    def __collect_information(self, ad_data):
        nan = float("nan")
        try:
            self.url = ad_data["url"]
        except:
            pass
        try:
            self.rent = ad_data["rent"]["amount"] / 100
        except:
            pass
        try:
            self.description = ad_data["description"][:1000]
        except:
            pass
        try:
            self.latitude = ad_data["location"]["latitude"]
        except:
            pass
        try:
            self.longitude = ad_data["location"]["longitude"]
        except:
            pass
        try:
            self.address = ad_data["location"]["mapAddress"]
        except:
            pass
        try:
            self.province = ad_data["location"]["province"]
        except:
            pass
        try:
            self.utilities = ad_data["utility"]
        except:
            pass
        try:
            self.Bedrooms = ad_data["Bedrooms"]
        except:
            pass
        try:
            self.Bathrooms = ad_data["Bathrooms"]
        except:
            pass
        try:
            self.furnished = ad_data["Furnished"]
        except:
            pass
        try:
            self.__dict__["For Rent By"] = ad_data["For Rent By"]
        except:
            pass
        try:
            self.__dict__["Pet Friendly"] = ad_data["Pet Friendly"]
        except:
            pass
        try:
            self.laundry = ad_data["laundry"]
        except:
            pass
        try:
            adattrs = ad_data["adAttributes"]
            try:
                for an_attribute in adattrs:
                    key = an_attribute["localeSpecificValues"]["en"]["label"]
                    if key in COLUMN_NAMES:
                        self.__dict__[key] = an_attribute["localeSpecificValues"]["en"]["value"]
            except KeyError:
                pass  # key adAttributes was not found
        except:
            pass

    def __str__(self):
        return (
            f"Advertisement with id {self.__adId} costs ${self.__rent} at {self.__address}"
        )

    def get_json(cls):
        return cls.__dict__


class KijijiScraper_AnAdvertisement(object):
    def __init__(self, soup: BeautifulSoup):
        self.__data = (
            soup.find("div", {"id": "FesLoader"})
            .contents[1]
        )
        self.__data = json.loads(str(self.__data)[31 + 14 : -10])
        self.__nan = float("nan")

    def get_adId(self):
        try:
            return self.__data["config"]["VIP"]["adId"]
        except:
            return self.__nan

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
