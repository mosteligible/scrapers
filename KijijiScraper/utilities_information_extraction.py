import json
import spacy
from tqdm import tqdm
from nltk import word_tokenize
from string import punctuation
from random import sample

FILENAME = "data.json"


def read_file():
    with open(FILENAME, "r") as f:
        data = json.load(f)

    return data


def collect_descriptions(all_advertisements):
    nlp = spacy.load("en_core_web_sm")
    descriptions = []

    for an_advertisement in tqdm(all_advertisements, position=0):
        buffer = {}
        buffer["adId"] = an_advertisement["adId"]
        to_lemmatize = " ".join(
            [
                i.lower()
                for i in word_tokenize(an_advertisement["data"]["description"])
                if (i not in punctuation and i != "br")
            ]
        )
        to_lemmatize = nlp(to_lemmatize)

        to_lemmatize = " ".join([word.lemma_ for word in to_lemmatize])

        buffer["description"] = to_lemmatize
        descriptions.append(buffer)

    return descriptions


def get_descriptions(n=None):
    all_advertisements = read_file()
    if n != None:
        return collect_descriptions(sample(all_advertisements, n))
    else:
        return collect_descriptions(all_advertisements)


def main():
    descs = get_descriptions()
    only_descs = [i["description"] for i in descs]
    descs_keys = [i["adId"] for i in descs]
    only_descs_tokenized = [word_tokenize(i) for i in only_descs]

    keywords = [  #'heat',
        "hydro",
        #'wifi',
        #'ac',
        "utilities",
        "utility",
        #'water',
        #'parking',
        "free",
        "include",
        "included",
    ]

    result = []
    nan = float("nan")
    count_of_all = 0
    for i, a_description in enumerate(only_descs_tokenized):
        ceiling = len(a_description)
        count = 0
        counted_descriptions = 0
        selected = {}
        for indx, word in enumerate(a_description):

            top = ceiling if indx + 5 >= ceiling else indx + 5
            bottom = 0 if indx - 5 < 0 else indx - 5

            sliced = a_description[bottom:top]
            bool_in_slice = (
                ("free" in sliced and "utility" in sliced)
                or ("include" in sliced and "utility" in sliced)
                or ("hydro" in sliced and "include" in sliced)
                or ("unlimited" in sliced and "hydro" in sliced)
                or ("inclusive" in sliced and "utility" in sliced)
            )
            if word in keywords:
                # print(f'{i} : {a_description[bottom:top]}, {bool_in_slice}')
                counted_descriptions += 1
                if bool_in_slice:
                    count += 1
        try:
            avg = count / counted_descriptions
            selected["adId"] = descs_keys[i]
            if avg >= 0.5:
                selected["utility"] = True
            else:
                selected["utility"] = False
                count_of_all += 1
        except ZeroDivisionError:
            print(f"\n{descs_keys[i]}  caused zero division error")
            count_of_all += 1
            selected["utility"] = nan
        #        print(f'total counts: {count_of_all}')
        result.append(selected)

    return result


if __name__ == "__main__":
    result = main()
    with open("utility.json", "w+") as f:
        json.dump(result, f)
