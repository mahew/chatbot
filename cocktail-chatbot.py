#!/usr/bin/env python3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import json, requests
import aiml
import matplotlib.pyplot as plt
import csv

URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/"

with open('cocktailQA.csv') as f:
    reader = csv.reader(f, skipinitialspace=True)
    result = dict(reader)
    print(result)

def api(req, search = ""):
    if req == "define":
        define_url = r"search.php?s=" + search
        response = get_json_response(define_url)
        if response != False:
            print("Here is a {}!".format(search))
            show_cocktail(response)
            return "Anything else you would like to know?"
            
    elif req == "search-ingredient":
        pass

    elif req == "random":
        rand_url = r"random.php"
        response = get_json_response(rand_url)
        if response != False:
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

def calculate_tf_idf(s):
    return vec.fit_transform(s)

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

    elif answer[0] == '|':
        entry = answer[1:]
        # Need to make the string iterable, [] makes string into list
        try:
          entry_vector = vec.fit_transform([entry])
          for x in CSV:
            x_vector = vec.fit_transform([x])
            # For debugging to see all simularities
            entry_x_similarity = cosine_similarity(entry_vector, x_vector)
            print("Vector entry: {} Simularity: {}\n".format(x, entry_x_similarity))
            if entry_x_similarity > 0.8:
              answer = kern.respond(x)
              print(answer)
        except ValueError:
          # Might all be stop words, nothing to do now
          print("I don't understand what you mean! Sorry!")

    else:
        print(answer)