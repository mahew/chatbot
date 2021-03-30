import aiml

# aiml kernel used to provide reponses from xml file
kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="./data/cocktail-chatbot.xml")
