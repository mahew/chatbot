#!/usr/bin/env python3
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import json, requests
import aiml
import matplotlib.pyplot as plt

URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/"

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


kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="cocktail-chatbot.xml")

print("Welcome to the cocktail chat bot! Feel free to ask me about cocktails :)")

while True:

    try:
        userInput = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Exiting - Goodbye!")
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
    else:
        print(answer)