from simpful import FuzzySystem, TriangleFuzzySet, LinguisticVariable, AutoTriangle

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

def fuzzy(search):
    replys = []

    try:
        alchol_input = int(input("Enter the rough Alcohol % of " + search + " [0-100]> "))
        sweetness_input = int(input("Enter the rough sweetness of " + search + " [0-100]> "))
        FS.set_variable("alcohol", alchol_input) 
        FS.set_variable("sweetness", sweetness_input) 
        smoothness = FS.inference()
        print(smoothness)
        if smoothness["smoothness"] < 33:
            replys.append("The " + search + " might be quite harsh! Drink carefully")
        elif smoothness["smoothness"] < 66:
            replys.append("The " + search + " will be alright, but might tingle")
        else:
            replys.append("The " + search + " will be very smooth, enjoy!")
            
    except Exception:
        replys.append("Sorry, you provided an incorrect input, please try asking again")

    return replys