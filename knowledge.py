import sys
from nltk.sem import Expression
from nltk.inference import ResolutionProver
import pandas

# expression for NLP, knowledge base intialisation
read_expr = Expression.fromstring
kb=[]
data = pandas.read_csv('./data/kb.csv', header=None)
[kb.append(read_expr(row)) for row in data[0]]
#If we enter a blank expression, the KB will check for contradictions, 
#returning true if there is a problem
answer=ResolutionProver().prove("", kb, verbose=False)
if answer:
   print("Contradiction with the knowledge base, exiting")
   sys.exit()

def add_knowledge(statement, verbose=False):
    replys = []
    object, subject = statement.split(' is ')
    expr=read_expr(subject + '(' + object + ')')
    print(expr)
    kb.append(expr) 
    answer=ResolutionProver().prove(expr, kb, verbose=verbose)
    if answer:
        replys.append("OK, I will remember that {} is {}".format(object, subject))
    else:
        kb.remove(expr)
        replys.append("This is contradicting! I have ignored you.")
        
    replys.append("Anything else you would like to know?")
    return replys

def check_knowledge(statement, verbose=False):
    # check that * is *"
    replys = []
    object, subject = statement.split(' is ')
    raw_expr = subject + '(' + object + ')'
    expr=read_expr(raw_expr)
    answer=ResolutionProver().prove(expr, kb, verbose=verbose)
    if answer:
        replys.append("That is Correct!")
    else:
        if "not" in subject:
            subject = subject.replace("not", "")
        else:
            subject = "not " + subject
        expr=read_expr(subject + '(' + object + ')')
        answer=ResolutionProver().prove(expr, kb, verbose=verbose)
        if answer:
            replys.append("This is definitely false")
        else:
            replys.append("Sorry I don't know.")
        
    replys.append("Anything else you would like to know?")
    return replys