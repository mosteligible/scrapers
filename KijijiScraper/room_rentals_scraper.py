import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from string import punctuation
from nltk import word_tokenize
import spacy
from utils import KijijiScraper_AnAdvertisement
from sys import getsizeof


def preprocess_description(description) -> str:
    nlp = spacy.load("en_core_web_sm")
    description = " ".join(
        [
            i.lower()
            for i in word_tokenize(description)
            if (i not in punctuation and i != "br")
        ]
    )
    description = nlp(description)

    description = [word.lemma_ for word in description]

    return description


def is_utility_included(description: str) -> bool:
    keywords = ["hydro", "utilities", "utility", "inclusive", "free", "include", "included"]
    ceiling = len(description)
    count = 0
    counted_descriptions = 0
    for indx, word in enumerate(description):
        top = ceiling if indx + 5 >= ceiling else indx + 5
        bottom = 0 if indx - 5 < 0 else indx - 5

        sliced = description[bottom:top]
        bool_in_slice = (
            ("free" in sliced and "utility" in sliced)
            or ("include" in sliced and "utility" in sliced)
            or ("hydro" in sliced and "include" in sliced)
            or ("unlimited" in sliced and "hydro" in sliced)
            or ("inclusive" in sliced and "utility" in sliced)
            or ("all" in sliced and "inclusive" in sliced)
        )
        laundry_in_slice = not ("no" in sliced and "laundry" in sliced)
        if laundry_in_slice:
            laundry_in_slice = "laundry" in sliced
        if word in keywords:
            # print(f'{i} : {a_description[bottom:top]}, {bool_in_slice}')
            counted_descriptions += 1
            if bool_in_slice:
                count += 1
    try:
        avg = count / counted_descriptions
        if avg >= 0.5:
            return True, laundry_in_slice
        else:
            return False, laundry_in_slice
    except ZeroDivisionError:
        print(f"\nZero division error")
        return float("nan"), laundry_in_slice


def advertisement_details(url: str) -> dict:
    """
    This function takes in the link to an advertisement and returns the content
    of the page.
    """
    a_scraped_ad = KijijiScraper_AnAdvertisement(url)

    advertisementData = {}

    adId = a_scraped_ad.get_adId()
    advertisementData["adType"] = a_scraped_ad.get_adType()
    advertisementData["rent"] = a_scraped_ad.get_rent()
    advertisementData["description"] = a_scraped_ad.get_description()
    advertisementData["location"] = a_scraped_ad.get_location()
    description = preprocess_description(advertisementData["description"])
    advertisementData["utility"], advertisementData["laundry"] = is_utility_included(
        description
    )
    adAttributes = a_scraped_ad.get_adAttributes()
    for an_attribute in adAttributes:
        key = an_attribute["localeSpecificValues"]["en"]["label"]
        advertisementData[key] = an_attribute["localeSpecificValues"]["en"]["value"]

    return adId, advertisementData


def get_page_data(url: str) -> list:
    """
    This function takes in a response object and extracts the links to all the
    advertisement in the page, stores them in a list and returns it.
    For example, if there are 15 advertisement in current page, link to them
    will be stored in a list.

    This link will be used to scrape detailed information about those collected
    pages.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    ad_data = []

    regular_postings = soup.find_all("div", {"class": "search-item regular-ad"})
    broken_url = urlparse(url)
    # print("\nCollecting information from main page!..\n")
    for a_posting in tqdm(regular_postings, position=0):
        href = a_posting.find("a", {"class": "title"}).get(
            "href"
        )  # , a_posting.find('div',{'class':'price'}).text.strip()
        # break url into different parts
        # this is necessary because subsequent search requires to add the netloc
        # with main advertisement posts
        new_posting = broken_url.scheme + "://" + broken_url.netloc + href

        an_ad = {}
        an_ad["adId"], an_ad["data"] = advertisement_details(new_posting)
        ad_data.append(an_ad)

    return ad_data


def are_two_equal(a, b):
    return a == b


def main():
    # select page number 1
    current_page_no = 1

    # set url for page 1 of search
    # LONG TERM RENTALS
    # url=f'https://www.kijiji.ca/b-short-term-rental/ottawa/page-{current_page_no}/c42l1700185'

    # SHORT TERM RENTALS
    # url=f'https://www.kijiji.ca/b-short-term-rental/ottawa/page-{current_page_no}/c42l1700185'

    # ROOM RENTALS AND ROOMMATES
    url = f"https://www.kijiji.ca/b-room-rental-roommate/ottawa/page-{current_page_no}/c36l1700185"
    flag = True

    # get the number of pages search result is spread in
    # all_page_numbers = get_page_numbers(url)
    print(f"*****COLLECTING FROM {current_page_no}*********")
    # store the results in a dictionary, based on the number of pages
    all_results = []
    previous_page_data = get_page_data(url)
    all_results.extend(previous_page_data)
    previous_page_id = [i["adId"] for i in previous_page_data]
    del previous_page_data
    print("******************DONE*************************\n\n")
    while flag:
        # set url to update for each iteration
        current_page_no += 1
        # LONG TERM RENTALS
        # url=f'https://www.kijiji.ca/b-short-term-rental/ottawa/page-{current_page_no}/c42l1700185'

        # SHORT TERM RENTALS
        # url=f'https://www.kijiji.ca/b-short-term-rental/ottawa/page-{current_page_no}/c42l1700185'

        # ROOM RENTALS AND ROOMMATES
        url = f"https://www.kijiji.ca/b-room-rental-roommate/ottawa/page-{current_page_no}/c36l1700185"
        print(f"*****COLLECTING FROM {current_page_no}*********")
        print(url)
        page_data = get_page_data(url)
        current_page_ids = [i["adId"] for i in page_data]
        if are_two_equal(previous_page_id, current_page_ids):
            break
        all_results.extend(page_data)
        previous_page_id = current_page_ids.copy()
        print("******************DONE*************************\n\n")


def main():
    # select page number 1
    current_page_no = 1

    # set url for page 1 of search
    # LONG TERM RENTALS
    # url=f'https://www.kijiji.ca/b-short-term-rental/ottawa/page-{current_page_no}/c42l1700185'

    # SHORT TERM RENTALS
    # url=f'https://www.kijiji.ca/b-short-term-rental/ottawa/page-{current_page_no}/c42l1700185'

    # ROOM RENTALS AND ROOMMATES
    url = f"https://www.kijiji.ca/b-room-rental-roommate/ottawa/page-{current_page_no}/c36l1700185"
    flag = True

    # get the number of pages search result is spread in
    # all_page_numbers = get_page_numbers(url)
    print(f"*****COLLECTING FROM {current_page_no}*********")
    # store the results in a dictionary, based on the number of pages
    all_results = []
    previous_page_data = get_page_data(url)
    all_results.extend(previous_page_data)
    previous_page_id = [i["adId"] for i in previous_page_data]
    del previous_page_data
    print("******************DONE*************************\n\n")
    while flag:
        # set url to update for each iteration
        current_page_no += 1
        # LONG TERM RENTALS
        # url=f'https://www.kijiji.ca/b-short-term-rental/ottawa/page-{current_page_no}/c42l1700185'

        # SHORT TERM RENTALS
        # url=f'https://www.kijiji.ca/b-short-term-rental/ottawa/page-{current_page_no}/c42l1700185'

        # ROOM RENTALS AND ROOMMATES
        url = f"https://www.kijiji.ca/b-room-rental-roommate/ottawa/page-{current_page_no}/c36l1700185"

        print(f"*****COLLECTING FROM {current_page_no}*********")
        print(url)
        page_data = get_page_data(url)
        current_page_ids = [i["adId"] for i in page_data]
        if are_two_equal(previous_page_id, current_page_ids):
            break

        all_results.extend(page_data)
        previous_page_id = current_page_ids.copy()

        print("******************DONE*************************\n\n")

        if getsizeof(all_results) / 1024 > 500:
            COUNTERSTR = "./room_rentals_data_json/counter.txt"
            try:
                with open(COUNTERSTR, "r") as f_counter:
                    counter = int(f_counter.readline())
            except FileNotFoundError:
                counter = 0

            jsonFileName = f"./room_rentals_data_json/data{counter+1}.json"

            with open(jsonFileName, "w") as f:
                json.dump(result, f)
            with open(COUNTERSTR, "w") as f_counter:
                f_counter.write(str(counter + 1))

            all_results = []

    return all_results


if __name__ == "__main__":
    # SHORT TERM RENTALS
    # counter_str='./short_term_rentals_data_json/counter.txt'

    # LONG TERM RENTALS
    # counter_str='./data/counter.txt'

    # ROOM RENTALS AND ROOMMATES
    COUNTERSTR = "./room_rentals_data_json/counter.txt"
    try:
        with open(COUNTERSTR, "r") as f_counter:
            counter = int(f_counter.readline())
    except FileNotFoundError:
        print("This is the first time we are scraping this page!")
        counter = 0
    result = main()

    try:
        with open(COUNTERSTR, "r") as f_counter:
            counter = int(f_counter.readline())
    except:
        pass
    # SHORT TERM RENTALS
    # jsonFileName=f'./short_term_rentals_data_json/data{counter+1}.json'

    # LONG TERM RENTALS
    # jsonFileName=f'./data/data{counter+1}.json'

    # ROOM RENTALS AND ROOMMATES
    jsonFileName = f"./room_rentals_data_json/data{counter+1}.json"

    with open(jsonFileName, "w") as f:
        json.dump(result, f)
    with open(COUNTERSTR, "w") as f_counter:
        f_counter.write(str(counter + 1))
