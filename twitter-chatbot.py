import aiml
import wikipedia
import json, requests
import twitterlib as twitter

kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="C:\\Users\\Mahew\OneDrive\OneDrive - Nottingham Trent University\\Year 4\\AI Term 1\\Coursework 1\\twitter-chatbot.xml")

print("Enter a twitter handle")

#=====================================================================================

while True:
    #get user input
    try:
        userInput = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye!")
        break
    #pre-process user input and determine response agent (if needed)
    responseAgent = 'aiml'
    #activate selected response agent
    if responseAgent == 'aiml':
        answer = twitter.get_user_details(userInput)
        #answer = kern.respond(userInput)
    #post-process the answer for commands
    if answer.length > 0 & answer[0] == '#':
        params = answer[1:].split('$')
        cmd = int(params[0])
        if cmd == 0:
            print(params[1])
            break
        elif cmd == 1:
            try:
                wSummary = wikipedia.summary(params[1], sentences=3,auto_suggest=False)
                print(wSummary)
            except Exception:
                print("Sorry, I do not know that. Be more specific!")
        elif cmd == 99:
            print("I did not get that, please try again.")
    else:
        print(answer)