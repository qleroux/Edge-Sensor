from weioLib.weio import *
import datetime
import urllib2
from things.input.distance.HCSR04 import HCSR04

def setup():
    attach.process(readHCSR04)
    
### ---------------------------------------------
## ----------------------------------------------
# SENSORS ---------------------------------------


def readHCSR04():
    Results = []
    emonApiKey="7d0f06aad70d20f9aad14f85d8a68be4"
    
    while True:
        Results.append(HCSR04(0,1).distCentimeters())
        if len(Results) == 5: #5 is good
            moyennedesresultats = int(moyenne(sansaberation(Results)))
            serverPush("P", moyennedesresultats)
            Results = []
            # url  ="http://emoncms.org/input/post.json?node=1&apikey=7d0f06aad70d20f9aad14f85d8a68be4&json={dist:" + "%.2f"%moyennedesresultats  + "}"
            # url = "http://api.thingspeak.com/update.json?api_key=SUBNBWNSUM1EVR2R&field1="+ "%.2f"%moyennedesresultats +"&field2=proche"
            # urllib2.urlopen(url)
        delay(100) # wait 0.1 second (100)
     
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