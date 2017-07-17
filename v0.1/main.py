from weioLib.weio import *
from things.input.distance.HCSR04 import HCSR04

def setup():
    attach.process(readHCSR04)
    # attach.process(readDHT11)
    # attach.process(readVMA309)
    
### ---------------------------------------------
## ----------------------------------------------
# SENSORS ---------------------------------------


def readHCSR04():
    Results = []
    while True:
        Results.append(HCSR04(0,1).distCentimeters())
        if len(Results) == 5: #5 is good
            moyennedesresultats = int(moyenne(sansaberation(Results)))
            serverPush("P", moyennedesresultats)
            Results = []
        delay(100) # wait 0.1 second (100)
        
def readDHT11():
    while True:
        data = dhtRead(8)
        print(data)
        serverPush("HT", [data[0], data[2]])
        delay(5000)

def readVMA309():
    average = 0
    count = 0
    while True:
        print(analogRead(24))
        average += analogRead(24)
        count += 1
        if count == 10:
            serverPush("S", average/10)
            average = 0
            count = 0
        delay(1000)



     
### ---------------------------------------------
## ----------------------------------------------
# FONCTIONS MATH --------------------------------

def moyenne(tableau):
    return sum(tableau, 0.0) / float(len(tableau))

def variance(tableau):
    m=moyenne(tableau)
    return moyenne([(x-m)**2 for x in tableau])
    
def ecartype(tableau):
    return variance(tableau)**0.5
    
def borneinferieure(tableau):
    return moyenne(tableau) - ecartype(tableau)
    
def bornesuperieure(tableau):
    return moyenne(tableau) + ecartype(tableau)

def sansaberation(tableau):
    BS = int(bornesuperieure(tableau))
    BI = int(borneinferieure(tableau))
    newtableau = []
    count = 0
    for i in tableau:
        count+=1
        if (i <= BS and i >= BI):
            newtableau.append(i)
        if(count == len(tableau)):
            return newtableau