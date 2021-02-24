from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
from nltk.sem import Expression
from nltk.inference import ResolutionProver
import tkinter as tk
from tkinter import filedialog
import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
#import matplotlib.pyplot as plt
import json, requests
import pandas
import aiml
import sys
import csv
import warnings
from simpful import *

##############################################################################
FS = FuzzySystem()

LowT = TriangleFuzzySet(4,7,14,   term="low")
MedT = TriangleFuzzySet(10,12,40,  term="medium")
HighT = TriangleFuzzySet(14,40,100, term="high")
FS.add_linguistic_variable("alcohol", LinguisticVariable([LowT, MedT, HighT], 
                 concept="Alcohol Strength %", universe_of_discourse=[0,100]))


TLV = AutoTriangle(3, terms=['low', 'medium', 'high'], universe_of_discourse=[0,100])
FS.add_linguistic_variable("sweetness", TLV)

SAT = AutoTriangle(3, terms=['harsh', 'average', 'smooth'], universe_of_discourse=[0,100])
FS.add_linguistic_variable("smoothness", SAT)

FS.add_rules([
	"IF (alcohol IS high) THEN (smoothness IS harsh)",
	"IF (alcohol IS low) THEN (smoothness IS smooth)",
    "IF (alcohol IS medium) AND (sweetness IS low) THEN (smoothness IS average)",
	"IF (alcohol IS medium) AND (sweetness IS high) THEN (smoothness IS high)"
	])

#FS.produce_figure(outputfile='plot.pdf')
##############################################################################

##############################################################################
img_height = 256
img_width = 256
cnn_model = tf.keras.models.load_model('chatbot_model.h5')
class_names = ['beer', 'cocktail', 'wine']
##############################################################################

##############################################################################
# expression for NLP, knowledge base intialisation
read_expr = Expression.fromstring
kb=[]
data = pandas.read_csv('kb.csv', header=None)
[kb.append(read_expr(row)) for row in data[0]]
#If we enter a blank expression, the KB will check for contradictions, 
#returning true if there is a problem
answer=ResolutionProver().prove("", kb, verbose=True)
if answer:
   print("Contradiction with the knowledge base, exiting")
   sys.exit()
##############################################################################

##############################################################################
# base url for the cocktail api
URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/"
##############################################################################

##############################################################################
# read the csv file as a dict object
CSV = {}
with open('cocktailQA.csv') as f:
    reader = csv.reader(f, skipinitialspace=True)
    CSV = dict(reader)
##############################################################################


# api function to provide information from www.thecocktaildb.com 
def api(req, search = ""):
    try:
        if req == "cnn":
            print("Hmmmm.... let me take a look at it, can you provide the file?")
            root = tk.Tk()
            root.withdraw()        
            file_path = filedialog.askopenfilename()
            root.lift()
            
            img = keras.preprocessing.image.load_img(
                file_path, target_size=(img_height, img_width)
            )
            
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
            
            predictions = cnn_model.predict(img_array)
            score = tf.nn.softmax(predictions[0])
            confidence = 100 * np.max(score)
            
            if confidence < 70:
                print("I'm not very sure what this is, sorry! Try ask me what something else is")
            else:
                print(
                    "This image is most likely a {} I have {:.2f} percent confidence in my predicion."
                    .format(class_names[np.argmax(score)], confidence)
                )
            
            return "Anything else you would like to know?"
    
        elif req == "define":
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
            
        elif req == "fuzzy":
            try:
                alchol_input = int(input("Enter the rough Alcohol % of " + search + " [0-100]> "))
                sweetness_input = int(input("Enter the rough sweetness of " + search + " [0-100]> "))
                FS.set_variable("alcohol", alchol_input) 
                FS.set_variable("sweetness", sweetness_input) 
                smoothness = FS.inference()
                print(smoothness)
                if smoothness["smoothness"] < 33:
                    print("The " + search + " might be quite harsh! Drink carefully")
                elif smoothness["smoothness"] < 66:
                    print("The " + search + " will be alright, but might tingle")
                else:
                    print("The " + search + " will be very smooth, enjoy!")
            except Exception as e:
                print("Sorry, you provided an incorrect input, please try asking again")
            return "Anything else you would like to know?"
    
        elif req == "knowledge":
            object, subject = search.split(' is ')
            expr=read_expr(subject + '(' + object + ')')
            print(expr)
            kb.append(expr) 
            answer=ResolutionProver().prove(expr, kb, verbose=True)
            if answer:
                kb.remove(expr)
                print("This is contradicting! I have ignored you.")
            else:
                print('OK, I will remember that',object,'is', subject)


            return "Anything else you would like to know?"
    
        elif req == "checkknowledge": 
            # check that * is *"
            object, subject = search.split(' is ')
            print(subject)
            raw_expr = subject + '(' + object + ')'
            expr=read_expr(raw_expr)
            answer=ResolutionProver().prove(expr, kb, verbose=True)
            if answer:
               return "That is Correct! Anything else you would like to know?"
            else:
               if "not" in subject:
                   subject = subject.replace("not", "")
               else:
                   subject = "not " + subject
               expr=read_expr(subject + '(' + object + ')')
               print(expr)
               answer=ResolutionProver().prove(expr, kb, verbose=True)
               if answer:
                   print("This is definitely false")
               else:
                   print("Sorry I don't know.")
               return "Anything else you would like to know?"

        elif req == "exit":
            # exit the program
            print("Goodbye! Have a good day!")
            sys.exit()

        # if not found, print a message
        else:
            return "I don't understand what you mean! Sorry!"

    except Exception as e:
      print(e)
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
    #plt.imshow(img)
    #plt.show()

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