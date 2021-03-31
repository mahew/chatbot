import sys
from fuzzy import fuzzy
from cnn import classify
from api import define, recipe, glass, ingredients, random
from knowledge import add_knowledge, check_knowledge
from kernel import kern
from simularity import get_similar_string
from language import output_replys, translate_text, get_input_lang

def process_input(gui, user_input):
    # process user input and determine response
    input_lang = get_input_lang(user_input)
    if input_lang == None:
        return ["I cant recognize this input! Sorry!"]
    elif input_lang != "en":
        # translate to english if not
        translated_input = translate_text(user_input, from_lang=input_lang)
        answer = kern.respond(translated_input)
    else:
        answer = kern.respond(user_input)
    
    # initiate replys 
    replys = []

    # check the answer for commands
    if answer[0] == '#':
        command_and_input = answer[1:].split('$')
        replys = get_replys(gui, command_and_input[0], command_and_input[1])
    # if no aiml command found, use bag of words with tf.idf cosine simularity to respond
    elif answer[0] == '|':
        replys = get_similar_string(answer)
    else:
        # standard string kernal reponse
        replys.append(answer)

    # output repsonses from the chatbot in the input lang
    replys = output_replys(replys, to_lang=input_lang)
    return replys

def get_replys(gui, command, input = ""):
    replys = []
    if command == "cnn":
        replys = classify(gui)
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