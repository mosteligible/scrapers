import spacy
from nltk import word_tokenize
import pandas as pd
from string import punctuation
from tqdm import tqdm


FILENAME = "./room_rentals_data_Accumulated/Advertisement_structured.csv"


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


def is_furnished(description):
    furnished = False
    laundry = float("nan")
    for a_word in description:
        # if a_word == 'furnished':
        #    furnished = True
        if "laundry" in a_word:
            laundry = True

    return furnished, laundry


def main(df):
    descriptions = df.description.to_list()

    furnished = []
    laundry = []
    for a_description in tqdm(descriptions, position=0):
        description = preprocess_description(a_description)
        furn, laund = is_furnished(description)
        laundry.append(laund)
        # furnished.append(furn)

    return furnished, laundry


if __name__ == "__main__":
    df = pd.read_csv(FILENAME, index_col=0)

    furnished, laundry = main(df)

    df["laundry"] = laundry
