"""
This file is used to read the scraped datas and get them in right format, save
as csv or any required format.
"""
from pathlib import Path
import pandas as pd
import json
from config import LONGTERM_JSON_PATH, LONGTERM_STRUCTURED
from constants import COLUMN_NAMES
from data_models import AnAdvertisement


def read_file(filename: Path) -> dict:
    """
    This function takes a json file name and returns the data in dictionary
    format.
    """
    with open(filename, "r") as f:
        data = json.loads(f)

    return data


def add_data(files_to_do):
    """
    This function takes in the list of files that have not been read or
    used to turn into structured data.
    The argument files_to_do contains a list of string that is name of files
    that have not been previously read into the structured data.

    Every entry on new file will be checked if it already exists in the
    structured file and will be added if it does not exist. Match is determined
    based on adId which is unique for each advertisement.

    It updates the already existing file with newest entries at the end.

    files_to_do: a list of string where each string entry is the name of file
                 that has not been processed

    returns: Nothing
    """
    csvFileName = "Advertisement_structured.csv"
    df = pd.read_csv(f"./{LONGTERM_STRUCTURED}/{csvFileName}", index_col=0)
    df.adId = df.adId.astype("int32")
    adIds = df.adId.to_list()
    indx = len(adIds)
    for a_file in files_to_do:
        with open(f"{LONGTERM_JSON_PATH}/{a_file}", "r") as f:
            data = json.load(f)
        print(f"\nWorking with data in {a_file}\n")
        for a_datapoint in data:
            segmented_data = AnAdvertisement(a_datapoint)

            if segmented_data.get_adid() not in adIds:
                df.loc[indx, "adId"] = segmented_data.get_adid()
                df.loc[indx, "description"] = segmented_data.get_description()
                df.loc[indx, "utilities"] = segmented_data.is_utilities_included()
                df.loc[indx, "rent"] = segmented_data.get_rent()
                df.loc[indx, "address"] = segmented_data.get_address()
                df.loc[indx, "province"] = segmented_data.get_province()
                df.loc[indx, "latitude"] = segmented_data.get_latitude()
                df.loc[indx, "longitude"] = segmented_data.get_longiutde()
                df.loc[indx, "Bedrooms"] = segmented_data.get_numBedrooms()
                df.loc[indx, "Bathrooms"] = segmented_data.get_numBathrooms()
                df.loc[indx, "Furnished"] = segmented_data.isFurnished()
                df.loc[indx, "For Rent By"] = segmented_data.who_is_renting()
                df.loc[indx, "Pet Friendly"] = segmented_data.is_pet_friendly()
                df.loc[indx, "laundry"] = segmented_data.get_laundry()

                adattrs = segmented_data.get_adAttributes()

                try:
                    for an_attribute in adattrs:
                        key = an_attribute["localeSpecificValues"]["en"]["label"]
                        df.loc[indx, key] = an_attribute["localeSpecificValues"]["en"][
                            "value"
                        ]
                except TypeError:
                    print(f'{df.loc[indx, "adId"]} has no ad Attribute')
                indx += 1

    df.to_csv(f"{LONGTERM_STRUCTURED}/Advertisement_structured1.csv")
