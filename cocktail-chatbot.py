#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
            response = requests.get(response["drinks"][0]["strDrinkThumb"], stream=True)
            img = Image.open(response.raw)
            plt.imshow(img)
            plt.show()
    elif req == "search-ingredient":
        pass
    elif req == "random-cocktail":
        rand_url = r"random.php"
        response = get_json_response(rand_url)
        if response != False:
            return response[""]
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

kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="cocktail-chatbot.xml")

print("Welcome to this chat bot. Please feel free to ask questions from me!")

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