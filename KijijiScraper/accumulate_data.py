"""
This file is used to read the scraped datas and get them in right format, save
as csv or any required format.
"""
import pandas as pd
import json
import os
from ScrapeModels import AnAdvertisement


# LONG TERM RENTALS
ACCUMULATED_DATA_LOCATION = "./longtermRentals_Accumulated"
DATA = "./longtermRentals_json"

# SHORT TERM RENTALS
# ACCUMULATED_DATA_LOCATION='./short_term_rentals_data_Accumulated'
# DATA='./short_term_rentals_data_json'

# ROOM RENTALS AND ROOMMATES
# ACCUMULATED_DATA_LOCATION = './room_rentals_data_Accumulated'
# DATA='./room_rentals_data_json'


def read_file(filename: str) -> str:
    """
    This function takes a json file name and returns the data in dictionary
    format.
    """
    with open(filename, "r") as f:
        data = json.load(f)

    return data


def initialize_dataframe():
    """
    This function is called when we have json data files but they have not been
    transformed into a csv or structured format.
    In this functino we create a dataframe with columns with names given below.

    utils.py files has a AnAdvertisement class that will take in each dictionary
    from json file which will be used to get relevant details from a dictionary

    It returns nothing but will save the structured data and a counter file
    that has name of json file which was turned into structured data.
    """
    column_names = [
        "adId",
        "address",
        "province",
        "latitude",
        "longitude",
        "rent",
        "utilities",
        "description",
        "Furnished",
        "Bathrooms",
        "Bedrooms",
        "For Rent By",
        "Pet Friendly",
        "Water",
        "Heat",
        "Hydro",
        "Agreement Type",
        "Parking Included",
        "Accessible Washrooms in Suite",
        "Internet",
        "Cable / TV",
        "Visual Aids",
        "Barrier-free Entrances and Ramps",
        "Audio Prompts",
        "Braille Labels",
        "Elevator in Building",
        "Storage Space",
        "Bicycle Parking",
        "24 Hour Security",
        "Concierge",
        "Pool",
        "Gym",
        "Smoking Permitted",
        "Balcony",
        "Yard",
        "Air Conditioning",
        "Fridge / Freezer",
        "Dishwasher",
        "Laundry (In Building)",
        "Laundry (In Unit)",
        "Wheelchair accessible",
        "building_access",
    ]

    df = pd.DataFrame(columns=column_names)

    files = os.listdir("./longtermRentals_json")[-1:]  # files=os.listdir(f'{DATA}')
    indx = 0
    for a_file in files:
        if a_file.endswith(".json"):
            data = read_file(f"{DATA}/{a_file}")
            for a_datapoint in data:
                segmented_data = AnAdvertisement(a_datapoint)

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
                indx += 1
                with open(f"{ACCUMULATED_DATA_LOCATION}/counter.txt", "w") as f:
                    f.write(f"{a_file}\n")
    df.to_csv(f"{ACCUMULATED_DATA_LOCATION}/Advertisement_structured.csv")


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
    df = pd.read_csv(f"./{ACCUMULATED_DATA_LOCATION}/{csvFileName}", index_col=0)
    df.adId = df.adId.astype("int32")
    adIds = df.adId.to_list()
    indx = len(adIds)
    for a_file in files_to_do:
        with open(f"{DATA}/{a_file}", "r") as f:
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
                indx += 1

    df.to_csv(f"{ACCUMULATED_DATA_LOCATION}/Advertisement_structured1.csv")


def main():
    import os

    was_accumulation_initialized = (
        True if len(os.listdir(ACCUMULATED_DATA_LOCATION)) > 0 else False
    )

    if not was_accumulation_initialized:
        print(f"This is first time structuring the data!")
        initialize_dataframe()
    else:
        json_files = os.listdir(f"{DATA}")
        json_files = [i for i in json_files if i.endswith(".json")]
        # with open(f'./{ACCUMULATED_DATA_LOCATION}/counter.txt','r') as f:
        #    completed_files = f.readlines()
        # completed_files = [i.strip() for i in completed_files]
        files_to_do = os.listdir("./longtermRentals_json")[
            -1
        ]  # [i for i in json_files if i not in completed_files]
        add_data(files_to_do)
        with open(f"./{ACCUMULATED_DATA_LOCATION}/counter.txt", "a") as f:
            for a_file_name in files_to_do:
                f.write(a_file_name + "\n")


if __name__ == "__main__":
    main()
