import json, requests
from PIL import Image
import matplotlib.pyplot as plt

# api functions to provide information from www.thecocktaildb.com 
# base url for the cocktail api
URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/"
SEARCH = r"search.php?s="

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

def define(search):
    replys = []
    # search the api for the given cocktail
    define_url = SEARCH + search
    response = get_json_response(define_url)
    if response != False:
        # show the cocktail image if a reponse if given
        show_cocktail(response)
        replys.append("Here is a {}!".format(search))
    else:
        replys.append("I can't find {}".format(search))

    return replys

def recipe(search):
    replys = []
    # gets the recipe for the given cocktail
    recipe_url = SEARCH + search
    response = get_json_response(recipe_url)
    if response != False:
        replys.append(response["drinks"][0]["strInstructions"])
    else:
        replys.append("I can't find {}".format(search))

    return replys

def glass(search):
    replys = []
    # gets the glass for the given cocktail
    glass_url = SEARCH + search
    response = get_json_response(glass_url)
    if response != False:
        replys.append(response["drinks"][0]["strGlass"])
    else:
        replys.append("Sorry I cant find the glass used for {}".format(search))

    return replys

def ingredients(search):
    replys = []
    ingredients_url = SEARCH + search
    response = get_json_response(ingredients_url)
    if response != False:
        drink = response["drinks"][0]
        # lists of all ingredients           
        ingredients = []
        ingredients.append(drink["strIngredient1"])
        ingredients.append(drink["strIngredient2"])
        ingredients.append(drink["strIngredient3"])
        ingredients.append(drink["strIngredient4"])
        ingredients.append(drink["strIngredient5"])
        ingredients.append(drink["strIngredient6"])
        ingredients.append(drink["strIngredient7"])
        ingredients.append(drink["strIngredient8"])
        # lists of all ingredients measures
        ingredient_measures = []
        ingredient_measures.append(drink["strMeasure1"])
        ingredient_measures.append(drink["strMeasure2"])
        ingredient_measures.append(drink["strMeasure3"])
        ingredient_measures.append(drink["strMeasure4"])
        ingredient_measures.append(drink["strMeasure5"])
        ingredient_measures.append(drink["strMeasure6"])
        ingredient_measures.append(drink["strMeasure7"])
        ingredient_measures.append(drink["strMeasure8"])
        # iterate the ingredients
        for x in range(8):
            # if ingredient is present, print it
            if ingredients[x] != None:
                # some ingredient have a measure, some are un measured
                if ingredient_measures[x] != None:
                    replys.append(ingredient_measures[x] + ingredients[x])
                else:
                    replys.append(ingredients[x])
    else:
        replys.append("Can't find the ingredients for {}".format(search))

    return replys

def random():
    # use random api for to get random cocktail
    replys = []
    rand_url = r"random.php"
    response = get_json_response(rand_url)
    if response != False:
        replys.append("I reccomend a " + response["drinks"][0]["strDrink"] + " , Here is a picture!")
        show_cocktail(response)
    else:
        replys.append("Sorry I cant find a random cocktail!")

    return replys
