from kernel import kern
from simularity import get_similar_string
from language import TextClient, output_replys, translate_text, get_input_lang, get_audio_input
from chatbot import get_replys

print("COCKTAIL CHATBOT - Ask me about Cocktails!")
while True:
    try:
        user_input = input("> ")  # keep getting user inputs until the program is exited
    except (KeyboardInterrupt, EOFError) as e:
        print("Exiting - Goodbye!", e)
        break
    
    # process user input and determine response
    input_lang = get_input_lang(user_input)
    if input_lang != "en":
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
        replys = get_replys(command_and_input[0], command_and_input[1])
    # if no aiml command found, use bag of words with tf.idf cosine simularity to respond
    elif answer[0] == '|':
        replys = get_similar_string(answer)
    else:
        # standard string kernal reponse
        replys.append(answer)

    # output repsonses from the chatbot in the input lang
    output_replys(replys, to_lang=input_lang)