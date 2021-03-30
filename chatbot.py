import sys
from fuzzy import fuzzy
from cnn import classify
from api import define, recipe, glass, ingredients, random
from knowledge import add_knowledge, check_knowledge

def get_replys(command, input = ""):
    replys = []
    if command == "cnn":
        replys = classify()
    elif command == "define":
        replys = define(input)      
    elif command == "recipe":
        replys = recipe(input)
    elif command == "glass":
        replys = glass(input)
    elif command == "ingredients":
        replys = ingredients(input)
    elif command == "random":
        replys = random()   
    elif command == "fuzzy":
        replys = fuzzy(input)
    elif command == "knowledge":
        replys = add_knowledge(input)
    elif command == "checkknowledge": 
        replys = check_knowledge(input)
    elif command == "exit":
        sys.exit()

    # if not found, print a message
    else:
        replys.append("I don't understand what you mean! Sorry!")
    
    return replys