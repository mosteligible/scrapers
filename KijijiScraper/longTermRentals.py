import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
import time
from utils import KijijiScraper_AnAdvertisement
import random


"""
def preprocess_description(description) -> str:
    nlp = spacy.load('en_core_web_sm')
    description = ' '.join([i.lower() for i in word_tokenize(description) if (i not in punctuation and i != 'br')])
    description = nlp(description)
    description = ([word.lemma_ for word in description])
    return description


def is_utility_included(description: str) -> bool:
    keywords = [#'heat',
                'hydro',
                #'wifi',
                #'ac',
                'utilities',
                'utility',
                #'water',
                #'parking',
                'free',
                'include',
                'included',
                ]
    ceiling=len(description)
    count=0
    counted_descriptions = 0
    for indx, word in enumerate(description):
        top=ceiling if indx+5>=ceiling else indx+5
        bottom=0 if indx-5<0 else indx-5

        sliced = description[bottom:top]
        bool_in_slice = ("free" in sliced and "utility" in sliced) or ("include" in sliced and 'utility' in sliced) or ('hydro' in sliced and 'include' in sliced) or ('unlimited' in sliced and 'hydro' in sliced) or ('inclusive' in sliced and 'utility' in sliced)
        if word in keywords:
            #print(f'{i} : {a_description[bottom:top]}, {bool_in_slice}')
            counted_descriptions+=1
            if bool_in_slice:
                count+=1
    try:
        avg= count/counted_descriptions
        if avg >= 0.5:
            return True
        else:
            return False
    except ZeroDivisionError:
        print(f'\nZero division error')
        return False
"""


def get_proxies():
    response = requests.get("https://www.us-proxy.org/")
    soup = BeautifulSoup(response.content, "lxml")
    proxies = soup.find("div", class_="modal-body")
    proxies = proxies.text.split("\n")[4:-1]
    return proxies


def advertisement_details(url: str) -> dict:
    """
    This function takes in the link to an advertisement and returns the content
    of the page.
    """
    count_retry = 0
    while True:
        try:
            a_scraped_ad = KijijiScraper_AnAdvertisement(url)  # , proxy)
            break
        except Exception as e:
            print(f"{e} error during reading page! Trying again, times {count_retry+1}")
            count_retry += 1
            if count_retry == 3:
                break
    if count_retry == 3:
        print(f"Could not read from page {url}")
        return "data could not be read!"

    advertisementData = {}

    adId = a_scraped_ad.get_adId()
    advertisementData["url"] = url
    advertisementData["adType"] = a_scraped_ad.get_adType()
    advertisementData["rent"] = a_scraped_ad.get_rent()
    advertisementData["description"] = a_scraped_ad.get_description()
    advertisementData["location"] = a_scraped_ad.get_location()
    # description = preprocess_description(advertisementData['description'])
    # advertisementData['utility'] = is_utility_included(description)
    advertisementData["adAttributes"] = a_scraped_ad.get_adAttributes()
    #    for an_attribute in adAttributes:
    #        key = an_attribute['localeSpecificValues']['en']['label']
    #        advertisementData[key] = an_attribute['localeSpecificValues']['en']['value']

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
    # proxies = get_proxies()
    regular_postings = soup.find_all("div", {"class": "search-item regular-ad"})
    broken_url = urlparse(url)
    # print("\nCollecting information from main page!..\n")
    for a_posting in regular_postings:
        time.sleep(1.5)
        href = a_posting.find("a", {"class": "title"}).get(
            "href"
        )  # , a_posting.find('div',{'class':'price'}).text.strip()
        # break url into different parts
        # this is necessary because subsequent search requires to add the netloc
        # with main advertisement posts
        new_posting = broken_url.scheme + "://" + broken_url.netloc + href
        # proxy = random.choice(proxies)
        an_ad = {}

        data_returned = advertisement_details(new_posting)  # , proxy)

        if data_returned == "data could not be read!":
            continue
        else:
            an_ad["adId"], an_ad["data"] = data_returned
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
    # url=f'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/page-{current_page_no}/c37l1700281?radius=5.0&ad=offering&address=1360+Ren%C3%A9-L%C3%A9vesque+Boulevard+West%2C+Montr%C3%A9al%2C+QC&ll=45.495802,-73.572627'
    # url= f'https://www.kijiji.ca/b-location-court-terme/ville-de-montreal/page-{current_page_no}/c42l1700281?radius=5.0&ad=offering&price=304__1200&address=Montr%C3%A9al%2C+QC&ll=45.501689,-73.567256'
    url = f"https://www.kijiji.ca/b-location-court-terme/ville-de-montreal/page-{current_page_no}/c42l1700281?radius=5.0&address=1360+Ren%C3%A9-L%C3%A9vesque+Boulevard+West%2C+Montr%C3%A9al%2C+QC&ll=45.495802,-73.572627"

    flag = True

    # get the number of pages search result is spread in
    # all_page_numbers = get_page_numbers(url)
    print(f"*****COLLECTING FROM {current_page_no}*********")
    # store the results in a dictionary, based on the number of pages
    all_results = []
    previous_page_data = get_page_data(url)
    all_results.extend(previous_page_data)
    previous_page_id = [i["adId"] for i in previous_page_data if type(i) != "str"]
    del previous_page_data
    print("******************DONE*************************\n\n")

    today_localtime = time.localtime()
    today_date = (
        f"{today_localtime.tm_year}-{today_localtime.tm_mon}-{today_localtime.tm_mday}"
    )

    while flag:
        # set url to update for each iteration
        current_page_no += 1
        # LONG TERM RENTALS
        url = f"https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/page-{current_page_no}/c37l1700281?radius=5.0&ad=offering&address=1360+Ren%C3%A9-L%C3%A9vesque+Boulevard+West%2C+Montr%C3%A9al%2C+QC&ll=45.495802,-73.572627"

        print(f"*****COLLECTING FROM {current_page_no}*********")
        print(url)
        page_data = get_page_data(url)

        if page_data == "data could not be read!":
            continue

        current_page_ids = [i["adId"] for i in page_data]
        if are_two_equal(previous_page_id, current_page_ids):
            break

        all_results.extend(page_data)
        previous_page_id = current_page_ids.copy()

        filename = "./longtermRentals_json/" + today_date + f" page-{current_page_no}.json"
        with open(filename, "w") as f:
            json.dump(page_data, f, indent=4)

        print("******************DONE*************************\n\n")

    return all_results


if __name__ == "__main__":
    # LONG TERM RENTALS
    COUNTERSTR = "./longtermRentals_json/counter.txt"
    try:
        with open(COUNTERSTR, "r") as f_counter:
            counter = int(f_counter.readline())
    except FileNotFoundError:
        print("This is the first time we are scraping this page!")
        counter = 0
    result = main()

    # SHORT TERM RENTALS
    # jsonFileName=f'./short_term_rentals_data_json/data{counter+1}.json'

    # LONG TERM RENTALS
    # jsonFileName=f'./data/data{counter+1}.json'

    # ROOM RENTALS AND ROOMMATES
    jsonFileName = f"./longtermRentals_json/data{counter+1}.json"

    with open(jsonFileName, "w") as f:
        json.dump(result, f)
    with open(COUNTERSTR, "w") as f_counter:
        f_counter.write(str(counter + 1))
