#!/usr/bin/env python3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import matplotlib.pyplot as plt
import json, requests
import aiml
import sys
import csv
import warnings

# base url for the cocktail api
URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/"

# read the csv file as a dict object
CSV = {}
with open('cocktailQA.csv') as f:
    reader = csv.reader(f, skipinitialspace=True)
    CSV = dict(reader)

# api function to provide information from www.thecocktaildb.com 
def api(req, search = ""):
  try:
    if req == "define":
        # search the api for the given cocktail
        define_url = r"search.php?s=" + search
        response = get_json_response(define_url)
        if response != False:
            # show the cocktail image if a reponse if given
            show_cocktail(response)
            print("Here is a {}!".format(search))
            return "Anything else you would like to know?"
            
    elif req == "recipe":
        # gets the recipe for the given cocktail
        recipe_url = r"search.php?s=" + search
        response = get_json_response(recipe_url)
        if response != False:
            print(response["drinks"][0]["strInstructions"])
            return "Anything else you would like to know?"

    elif req == "glass":
        # gets the glass for the given cocktail
        glass_url = r"search.php?s=" + search
        response = get_json_response(glass_url)
        if response != False:
            print(response["drinks"][0]["strGlass"])
            return "Anything else you would like to know?"

    elif req == "ingredients":
        ingredients_url = r"search.php?s=" + search
        response = get_json_response(ingredients_url)
        if response != False:
            # lists of all ingredients           
            ingredients = []
            ingredients.append(response["drinks"][0]["strIngredient1"])
            ingredients.append(response["drinks"][0]["strIngredient2"])
            ingredients.append(response["drinks"][0]["strIngredient3"])
            ingredients.append(response["drinks"][0]["strIngredient4"])
            ingredients.append(response["drinks"][0]["strIngredient5"])
            ingredients.append(response["drinks"][0]["strIngredient6"])
            ingredients.append(response["drinks"][0]["strIngredient7"])
            ingredients.append(response["drinks"][0]["strIngredient8"])
            # lists of all ingredients measures
            ingredient_measures = []
            ingredient_measures.append(response["drinks"][0]["strMeasure1"])
            ingredient_measures.append(response["drinks"][0]["strMeasure2"])
            ingredient_measures.append(response["drinks"][0]["strMeasure3"])
            ingredient_measures.append(response["drinks"][0]["strMeasure4"])
            ingredient_measures.append(response["drinks"][0]["strMeasure5"])
            ingredient_measures.append(response["drinks"][0]["strMeasure6"])
            ingredient_measures.append(response["drinks"][0]["strMeasure7"])
            ingredient_measures.append(response["drinks"][0]["strMeasure8"])
            # iterate the ingredients
            for x in range(8):
              # if ingredient is present, print it
              if ingredients[x] != None:
                # some ingredient have a measure, some are un measured, if a measure is present
                # print it
                if ingredient_measures[x] != None:
                  print(ingredient_measures[x] + ingredients[x])
                else:
                  print(ingredients[x])
            return "Anything else you would like to know?"

    elif req == "random":
        # use random api for to get random cocktail
        rand_url = r"random.php"
        response = get_json_response(rand_url)
        if response != False:
            print("I reccomend a " + response["drinks"][0]["strDrink"] + " , Here is a picture!")
            show_cocktail(response)
            return "Anything else you would like to know?"

    elif req == "exit":
        # exit the program
        print("Goodbye! Have a good day!")
        sys.exit()

    # if not found, print a message
    else:
        return "I don't understand what you mean! Sorry!"

  except Exception:
    print("I'm not sure what that is! Try asking me again")

def get_json_response(url):
    # use base url and additional url arguments provided
    response = requests.get(URL_BASE + url)
    if response.status_code == 200:
        response_json = json.loads(response.content)
        if response_json:
            # if the response is good, return the json as a dict object
            return response_json
        else:
            return False
    else:
         return False

def show_cocktail(cocktail_json):
    # get image of drink from api and use matplotlib to show it
    response = requests.get(cocktail_json["drinks"][0]["strDrinkThumb"], stream=True)
    img = Image.open(response.raw)
    plt.imshow(img)
    plt.show()

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

# aiml kernel used to provide reponses from xml file
kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="cocktail-chatbot.xml")

print("Welcome to the cocktail chat bot! Feel free to ask me about cocktails!")

while True:
    try:
        # keep getting user inputs until the program is exited
        userInput = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Exiting - Goodbye!")
        print(e)
        break

    #pre-process user input and determine response agent (if needed)
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
      try:
        # entry is got from aiml reponse
        entry = answer[1:]
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
          print(CSV[highest_simularity_string])
        else:
          print("I'm not quite sure what you mean! Try asking something else!")
      except Exception:
        print("I'm not quite sure what you mean! Try asking something else!")

    else:
        print(answer)