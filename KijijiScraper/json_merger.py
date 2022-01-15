"""
    MERGE JSONS
"""


import json
import os


def merge(location="./longtermRentals_json"):

    base = "C:\\Users\\Dell\\Documents\\Python Scripts\\Data For Good\\Housing project\\longtermRentals_json\\"
    files = os.listdir(base)
    all_data = []
    for a_file in files:
        print("Merging file:", a_file)
        if a_file.endswith(".txt"):
            continue
        with open(base + a_file, "r") as f:
            all_data.extend(json.load(f))

    with open(base + a_file.split(" ")[0] + "merged.json", "w") as f:
        json.dump(all_data, f, indent=2)


if __name__ == "__main__":
    merge()
