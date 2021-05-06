# coding: utf-8
import math
from Automates import *

fichier = open("Automates/int2-1-FA1.txt", "r")


def lire_automate_sur_fichier(fichier):
    split = fic.split()
    print(split)

    global NB_INITIAL_STATE, INITIAL_STATE, NB_FINAL_STATE, FINAL_STATE, NB_TRANSITIONS, TRANSITIONS
    i=0
    split_initial=split[i].split(':')
    NB_INITIAL_STATE=int(split_initial[1])
    print('NB_INITIAL_STATE = ' + str(NB_INITIAL_STATE))
    INITIAL_STATE=[]
    while (i < NB_INITIAL_STATE):
        i+=1
        INITIAL_STATE.append(split[i]) 
    print(INITIAL_STATE)

    i+=1
    split_final=split[i].split(':')
    NB_FINAL_STATE=int(split_final[1])
    print('\nNB_FINAL_STATE = ' + str(NB_FINAL_STATE))
    FINAL_STATE=[]
    while (i < NB_INITIAL_STATE+1+NB_FINAL_STATE):
        i+=1
        FINAL_STATE.append(split[i])
    print(FINAL_STATE)

    i+=1
    split_transitions=split[i].split(':')
    NB_TRANSITIONS=int(split_transitions[1])
    print('\nNB_TRANSITIONS = ' + str(NB_TRANSITIONS))
    TRANSITIONS=[]
    while (i < NB_INITIAL_STATE+NB_FINAL_STATE+NB_TRANSITIONS+2):
        TRANSITIONS.append(split[i+1])
        i+=1
    print(TRANSITIONS)

def afficher_automate():
    automate = 'INITIAL_STATE:'+str(NB_INITIAL_STATE)+'\n'
    for i in range(0,NB_INITIAL_STATE):
        automate += INITIAL_STATE[i]+'\n'
    automate += 'FINAL_STATE:'+str(NB_FINAL_STATE)+'\n'
    for i in range(0,NB_FINAL_STATE):
        automate += FINAL_STATE[i]+'\n'
    automate += 'TRANSITIONS:'+str(NB_TRANSITIONS)+'\n'
    for i in range(0,NB_TRANSITIONS):
        automate += TRANSITIONS[i]+'\n'

    print(automate)

def ecriture_automate_sur_fichier():
    fichier = open("Automate.txt", "w")

    automate = 'INITIAL_STATE:'+str(NB_INITIAL_STATE)+'\n'
    for i in range(0,NB_INITIAL_STATE):
        automate += INITIAL_STATE[i]+'\n'
    automate += 'FINAL_STATE:'+str(NB_FINAL_STATE)+'\n'
    for i in range(0,NB_FINAL_STATE):
        automate += FINAL_STATE[i]+'\n'
    automate += 'TRANSITIONS:'+str(NB_TRANSITIONS)+'\n'
    for i in range(0,NB_TRANSITIONS):
        automate += TRANSITIONS[i]+'\n'

    fichier.write(automate)
    fichier.close()
    print("Ecriture finis !")

def est_un_automate_assynchrone():
    i=0
    asynchrone=False
    global ASYNCHRONES
    ASYNCHRONES=[]
    while (i<NB_TRANSITIONS):
        if (TRANSITIONS[i].find("*")):
            asynchrone=True
            ASYNCHRONES.append(TRANSITIONS[i])
        i+=1
    if ASYNCHRONES:
        print(ASYNCHRONES)
    return(asynchrone)

#def elimination epsilon():

##### main #####

# fic
print("Start !\n")
fic = fichier.read()
fichier.close()
print (fic)

lire_automate_sur_fichier(fic)
print('\n')
#afficher_automate()

ecriture_automate_sur_fichier()
print(est_un_automate_assynchrone())

if not ASYNCHRONES:
    bus = []
    transit_epsilon = []
    print(INITIAL_STATE)
