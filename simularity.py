import csv
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from constants import UNSURE_STRING

# read the csv file as a dict object
CSV = {}
with open('./data/cocktailQA.csv') as f:
    reader = csv.reader(f, skipinitialspace=True)
    CSV = dict(reader)

def calculate_cosine_simularity(*strings): 
    vectors = [t for t in get_string_vectors(*strings)]
    # indexing the [0][1] gets us the single cosine simularity between the sentences
    # as calculating the differences produces a 2x2 matrix
    return cosine_similarity(vectors)[0][1]

def get_string_vectors(*strings):
    # get word vectors for the strings provided by using the tfidf vectorizer
    text = [t for t in strings]
    vectorizer = TfidfVectorizer(text)
    vectorizer.fit(text)
    return(vectorizer.transform(text).toarray())

def get_similar_string(input):
    replys = []
    try:
        # entry is got from aiml reponse
        entry = input[1:]
        # store local variables for highest simularity
        highest_simularity_string = '';
        highest_simularity = 0;
        for x in CSV:
          with warnings.catch_warnings():
            # ignore all caught warnings - commited by filter
            warnings.filterwarnings("ignore")
            # iterate all csv entries and find highest simularity
            entry_x_similarity = calculate_cosine_simularity(entry, x)
            if entry_x_similarity > highest_simularity:
              highest_simularity = entry_x_similarity
              highest_simularity_string = x
              #print("Vector entry: {} Simularity: {}\n".format(x, entry_x_similarity))
        # if simularity is high enough, print the answer from the csv file
        if highest_simularity > 0.5:  
          replys.append(CSV[highest_simularity_string])
        else:
          replys.append(UNSURE_STRING)
    except Exception:
        replys.append(UNSURE_STRING)
        
    return replys