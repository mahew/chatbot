#!/usr/bin/env python3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from PIL import Image
import json, requests
import aiml
import matplotlib.pyplot as plt
import csv
import warnings

URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/"

CSV = {}
with open('cocktailQA.csv') as f:
    reader = csv.reader(f, skipinitialspace=True)
    CSV = dict(reader)

def api(req, search = ""):
    if req == "define":
        define_url = r"search.php?s=" + search
        response = get_json_response(define_url)
        if response != False:
            print("Here is a {}!".format(search))
            show_cocktail(response)
            return "Anything else you would like to know?"
            
    elif req == "recipe":
        recipe_url = r"search.php?s=" + search
        response = get_json_response(recipe_url)
        if response != False:
            print(response["drinks"][0]["strInstructions"])
            return "Anything else you would like to know?"

    elif req == "glass":
        glass_url = r"search.php?s=" + search
        response = get_json_response(glass_url)
        if response != False:
            print(response["drinks"][0]["strGlass"])
            return "Anything else you would like to know?"

    elif req == "ingredients":
        glass_url = r"search.php?s=" + search
        response = get_json_response(glass_url)
        if response != False:

            ingredients = []
            ingredients.append(response["drinks"][0]["strIngredient1"])
            ingredients.append(response["drinks"][0]["strIngredient2"])
            ingredients.append(response["drinks"][0]["strIngredient3"])
            ingredients.append(response["drinks"][0]["strIngredient4"])
            ingredients.append(response["drinks"][0]["strIngredient5"])
            ingredients.append(response["drinks"][0]["strIngredient6"])
            ingredients.append(response["drinks"][0]["strIngredient7"])
            ingredients.append(response["drinks"][0]["strIngredient8"])

            ingredient_measures = []
            ingredient_measures.append(response["drinks"][0]["strMeasure1"])
            ingredient_measures.append(response["drinks"][0]["strMeasure2"])
            ingredient_measures.append(response["drinks"][0]["strMeasure3"])
            ingredient_measures.append(response["drinks"][0]["strMeasure4"])
            ingredient_measures.append(response["drinks"][0]["strMeasure5"])
            ingredient_measures.append(response["drinks"][0]["strMeasure6"])
            ingredient_measures.append(response["drinks"][0]["strMeasure7"])
            ingredient_measures.append(response["drinks"][0]["strMeasure8"])

            for x in range(8):
              if ingredients[x] != None:
                if ingredient_measures[x] != None:
                  print(ingredient_measures[x] + ingredients[x])
                else:
                  print(ingredients[x])

            return "Anything else you would like to know?"

    elif req == "random":
        rand_url = r"random.php"
        response = get_json_response(rand_url)
        if response != False:
            print("I reccomend a " + response["drinks"][0]["strDrink"] + " , Here is a picture!")
            show_cocktail(response)
            return "Anything else you would like to know?"

    else:
        return "I don't understand what you mean! Sorry!"

def get_json_response(url):
    response = requests.get(URL_BASE + url)
    if response.status_code == 200:
        response_json = json.loads(response.content)
        if response_json:
            return response_json
        else:
            return False
    else:
         return False

def show_cocktail(cocktail_json):
    response = requests.get(cocktail_json["drinks"][0]["strDrinkThumb"], stream=True)
    img = Image.open(response.raw)
    plt.imshow(img)
    plt.show()

def get_cosine_sim(*strs): 
    vectors = [t for t in get_vectors(*strs)]
    # indexing the [0][1] gets us the single cosine simularity between the sentences
    # as calculating the differences produces a 2x2 matrix
    return cosine_similarity(vectors)[0][1]
    
def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return(vectorizer.transform(text).toarray())

kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="cocktail-chatbot.xml")
vec = TfidfVectorizer(stop_words = 'english')
# If kern response is defaulted, we can use cosine simularity to check if the inputted command
# Is similar enough to another command, and then re run it through the aiml agent
print("Welcome to the cocktail chat bot! Feel free to ask me about cocktails :)")
while True:
    try:
        userInput = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Exiting - Goodbye!")
        print(e)
        break

    #pre-process user input and determine response agent (if needed)
    responseAgent = 'aiml'

    if responseAgent == 'aiml':
        answer = kern.respond(userInput)

    #post-process the answer for commands
    if answer[0] == '#':
        command = answer[1:].split('$')
        request = command[0]
        search = command[1]
        result = api(request, search)
        print(result)

    # if no aiml command found, use bag of words with tf.idf cosine simularity to respond
    elif answer[0] == '|':
        entry = answer[1:]
        # Need to make the string iterable, [] makes string into list
        highest_simularity = '';
        highest_simularity_vector = 0;
        for x in CSV:
          with warnings.catch_warnings():
            # ignore all caught warnings
            warnings.filterwarnings("ignore")
            # execute code that will generate warnings
            # For debugging to see all simularities
            entry_x_similarity = get_cosine_sim(entry, x)
            if entry_x_similarity > highest_simularity_vector:
              highest_simularity_vector = entry_x_similarity
              highest_simularity = x
            #print("Vector entry: {} Simularity: {}\n".format(x, entry_x_similarity))
        print(CSV[highest_simularity])
    else:
        print(answer)