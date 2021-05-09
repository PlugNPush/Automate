# coding: utf-8
import re
ASYNCHRONES=[]

fichier = open("Automates/B4-21.txt", "r")


def lire_automate_sur_fichier(fic):
    split = fic.split()
    print(split)

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
    LIBELLES=[]
    ETATS=[]
    while (i < NB_INITIAL_STATE+NB_FINAL_STATE+NB_TRANSITIONS+2):
        transition = split[i+1]
        transition_libelle=re.split(r'\d+', transition)[1] # ['','a','']
        transition_etats=re.split(r'\D+', transition) # ['1','2']
        TRANSITIONS.append(transition)
        if transition_libelle not in LIBELLES:
            LIBELLES.append(transition_libelle)
        if transition_etats[0] not in ETATS:
            ETATS.append(transition_etats[0])
        if transition_etats[1] not in ETATS:
            ETATS.append(transition_etats[1])
        i+=1
    print(TRANSITIONS)
    print('etats :',ETATS,'\nlibelles :',LIBELLES)
    return NB_INITIAL_STATE,INITIAL_STATE,NB_FINAL_STATE,FINAL_STATE,NB_TRANSITIONS,TRANSITIONS,ETATS,LIBELLES


def maj_libelles():
    global LIBELLES
    LIBELLES = []
    for trans in TRANSITIONS: # ajout des nouveaux libelles
        split_libelle = re.split(r'\d+', trans)[1]
        if split_libelle not in LIBELLES:
            LIBELLES.append(split_libelle) 
    print("maj_libelles:",LIBELLES)

def maj_etats():
    global ETATS
    ETATS = []
    for trans in TRANSITIONS: # ajout des nouveaux etats
        split_etats = re.split(r'\D+', trans)
        if split_etats[0] not in ETATS:
            ETATS.append(split_etats[0])
        if split_etats[1] not in ETATS:
            ETATS.append(split_etats[1])
    print("maj_etats:",ETATS)

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
    global ASYNCHRONES
    i=0
    asynchrone=False
    #ASYNCHRONES=[]
    while (i<NB_TRANSITIONS):
        if (TRANSITIONS[i].find('*') >= 0):
            asynchrone=True
            ASYNCHRONES.append(TRANSITIONS[i])
        i+=1
    if ASYNCHRONES:
        print('ASYNCHRONES :', ASYNCHRONES)
    return asynchrone


def elimination_epsilon():
    global NB_FINAL_STATE,FINAL_STATE,NB_TRANSITIONS,TRANSITIONS,ASYNCHRONES
    print('start :', ASYNCHRONES)
    while ASYNCHRONES:
        split_epsilon = ASYNCHRONES[0].split('*') # une transition vers un 'enfant'
        split_epsilon.insert(1, '*')
        #print('split_epsilon début :', ''.join(split_epsilon))
        transit_epsilon = [] # liste des transitions vers les 'petit-enfants'
        #print(split_epsilon[0])
        for i in TRANSITIONS: # recherche des 'petit-enfants'
            if i != ASYNCHRONES[0] and split_epsilon[2] == re.split(r'\D+', i)[0]:
                transit_epsilon.append(i)    
        print('split_epsilon :', split_epsilon,' transit_epsilon :', transit_epsilon)
        if len(transit_epsilon)==0: #or len(ajout_sortie)==0 : # transmission sortie à 1 transition
            if split_epsilon[0] not in FINAL_STATE and split_epsilon[2] in FINAL_STATE:
                FINAL_STATE.append(split_epsilon[0])
                NB_FINAL_STATE+=1
                print("ajout sortie ",split_epsilon[0])
            plusieurs_parents=False # virer la sortie de l'enfant
            for trans in TRANSITIONS:
                if split_epsilon[2] == re.split(r'\D+', trans)[1] and split_epsilon[0] != re.split(r'\D+', trans)[0]:
                    plusieurs_parents=True
            if not plusieurs_parents: # si enfant n'a qu'une seul transition précédente
                print("enleve sortie ",split_epsilon[2])
                if split_epsilon[2] in FINAL_STATE:
                    FINAL_STATE.remove(split_epsilon[2])
                    NB_FINAL_STATE-=1

        for i in transit_epsilon:
            nb_transition_enfant = 0
            for j in TRANSITIONS :
                if re.split(r'\D+', j)[1] == re.split(r'\D+', i)[0]:
                    nb_transition_enfant +=1
            split_epsilon[1]= re.split(r'\d+', i)[1]  # lettre ou * : ['','a','']  # 11*14 ou 21a2 (on ignore les chiffres)
            split_epsilon[2]= re.split(r'\D+', i)[1]  # chiffre ['0','0'] (on supprime la lettre)
            if split_epsilon[1]== '*':
                ASYNCHRONES.append(''.join(split_epsilon))
                #print('asynchrone append ',''.join(split_epsilon))
            TRANSITIONS.append(''.join(split_epsilon)) # création transition entre le 'parent' et les 'petit-enfants'
            NB_TRANSITIONS+=1
            
            #print('transition append ',''.join(split_epsilon))
            if nb_transition_enfant <= 1 :
                if i.find('*') != -1:
                    ASYNCHRONES.remove(i)
                    #print('asynchrone remove ', i)
                TRANSITIONS.remove(i)
                NB_TRANSITIONS-=1
                print('remove enfant ', i)
            #print('split_epsilon fin :', ''.join(split_epsilon))
        #INI FIN
        TRANSITIONS.remove(ASYNCHRONES[0]) # remove de l'enfant
        grand_parent=[]
        for e in TRANSITIONS:
            if re.split(r'\D+', e)[1] == ASYNCHRONES[0].split('*')[1]:
                grand_parent.append(e)
        # Supprimer un état sans famille autrefois relié à une sortie (il s'appelle Rémy)       
        if ASYNCHRONES[0].split('*')[1] in FINAL_STATE and len(grand_parent) <= 0:
            print("FORCE DELETE "+ ASYNCHRONES[0].split('*')[1])
            if ASYNCHRONES[0].split('*')[1] in FINAL_STATE:
                FINAL_STATE.remove(ASYNCHRONES[0].split('*')[1])
                NB_FINAL_STATE-=1
            # Après l'avoir complètement isolé, l'ascendance reprend le rôle de sortie   
            if ASYNCHRONES[0].split('*')[0] not in FINAL_STATE:
                FINAL_STATE.append(ASYNCHRONES[0].split('*')[0])
                NB_FINAL_STATE+=1
        # Ajouter une sortie à un état s'il est directement relié en ε à une autre sortie    
        if ASYNCHRONES[0].split('*')[1] in FINAL_STATE and ASYNCHRONES[0].split('*')[0] not in FINAL_STATE:
            FINAL_STATE.append(ASYNCHRONES[0].split('*')[0])
            NB_FINAL_STATE+=1        
        NB_TRANSITIONS-=1
        print('remove parent ', ASYNCHRONES[0], '\n')
        del ASYNCHRONES[0]
        #print(ASYNCHRONES)
    maj_libelles()
    maj_etats()

def determinisation_synchrone():
    global NB_INITIAL_STATE,INITIAL_STATE
    new_transitions=[]
    new_final=[]
    new_etats=[]
    new_libelles=[]
    new_enter=","
    for enter in INITIAL_STATE:
        new_enter += enter + ","
    new_etats.append(new_enter)
    INITIAL_STATE=[new_enter]
    NB_INITIAL_STATE=1
    # a placer dans une boucle
    for tr in TRANSITIONS:
        if ("," + re.split(r'\D+', tr)[0] + ",") in new_enter:
            if  re.split(r'\d+', tr)[1] not in new_libelles:
                new_libelles.append(re.split(r'\d+', tr)[1])
                liste_lib = {
                    re.split(r'\d+', tr)[1] : [re.split(r'\D+', tr)[1]]
                }
            else:
                liste_lib[re.split(r'\d+', tr)[1]].append(re.split(r'\D+', tr)[1])
    for keyll in liste_lib:
        new_suite=","
        for e in liste_lib[keyll]:
            new_suite += e + ","
        new_transitions.append(new_enter+keyll+new_suite)
        new_etats.append(new_suite)
    # fusion des entrées et de leurs transitions
    # ajout des transitions comme nouvel état
    # transmission des sorties (si dans les nouveaux états il y a un ancien comme sortie)
    # 

def standardisation(): # penser à mettre à jour ETATS avant !
    global NB_INITIAL_STATE,INITIAL_STATE,NB_FINAL_STATE,FINAL_STATE,NB_TRANSITIONS,TRANSITIONS
    if not est_un_automate_standard():
        enter=0
        while enter < len(INITIAL_STATE):
            transition_arrivantes=[]
            transition_sortantes=[]
            for i in TRANSITIONS: 
                if re.split(r'\D+', i)[1] == INITIAL_STATE[enter]:
                    transition_arrivantes.append(i)
                if re.split(r'\D+', i)[0] == INITIAL_STATE[enter]:
                    transition_sortantes.append(i)
            if len(transition_arrivantes)!=0:
                if 'I' not in ETATS: # verif pas nécessaire si testé au préalable
                    INITIAL_STATE.append('I')
                    NB_INITIAL_STATE+=1
                if INITIAL_STATE[enter] in FINAL_STATE and 'I' not in FINAL_STATE:
                    FINAL_STATE.append('I')
                    NB_FINAL_STATE+=1
                INITIAL_STATE.remove(INITIAL_STATE[enter])
                NB_INITIAL_STATE-=1
                enter-=1 # pas d'augmentation de enter à cause du remove
                for exite in transition_sortantes: # ajouter les transitions 'I..' + transition_sortante[1,2]
                    new_transition= 'I'+ re.split(r'\d+', exite)[1] + re.split(r'\D+', exite)[1]
                    print('new_transition :',new_transition)
                    TRANSITIONS.append(new_transition)
                    NB_TRANSITIONS+=1
            enter+=1
        print('\nStandardisation :\n',TRANSITIONS)
    else:
        print("\nL'automate est déjà standardisé !\n")
    
def est_un_automate_standard():
    global TRANSITIONS, INITIAL_STATE
    for i in TRANSITIONS:
        for e in INITIAL_STATE:
            if re.split(r'\D+', i)[1] == e:
                return False
    return True            

##### COMPLET ?
def est_un_automate_complet():
    global TRANSITIONS
    global ETATS
    global LIBELLES
    TRANS_COPY = []
    for e in TRANSITIONS:
        TRANS_COPY.append(re.split(r'\D+', e)[0] + re.split(r'\d+', e)[1])
    print(TRANS_COPY)
    for st in ETATS:
        for le in LIBELLES:
            tr = st+le
            if tr not in TRANS_COPY:
                return False
    return True

##### COMPLETION
def completion():
    global NB_TRANSITIONS
    global TRANSITIONS
    global ETATS
    global LIBELLES
    if not est_un_automate_complet():
        needsJunk = False
        TRANS_COPY = []
        for e in TRANSITIONS:
            TRANS_COPY.append(re.split(r'\D+', e)[0] + re.split(r'\d+', e)[1])
        print(TRANS_COPY)
        for st in ETATS:
            for le in LIBELLES:
                tr = st+le
                if tr not in TRANS_COPY:
                    needsJunk = True
                    TRANSITIONS.append(tr + "P")
                    NB_TRANSITIONS += 1
        if needsJunk:
            ETATS.append('P')
            for lettre in LIBELLES:
                TRANSITIONS.append("P" + lettre + "P")
                NB_TRANSITIONS+=1
        print(LIBELLES)
        print(ETATS)
        print(TRANSITIONS)

##### Complémentarisation
def automate_complementaire():
    global NOT_FINAL_STATE
    global NB_NOT_FINAL_STATE
    global FINAL_STATE
    global NB_FINAL_STATE
    NOT_FINAL_STATE = []
    NB_NOT_FINAL_STATE = 0
    for e in ETATS:
        if e not in FINAL_STATE:
            NOT_FINAL_STATE.append(e)
            NB_NOT_FINAL_STATE += 1
    NB_NOT_FINAL_STATE, NB_FINAL_STATE = NB_FINAL_STATE, NB_NOT_FINAL_STATE
    NOT_FINAL_STATE, FINAL_STATE = FINAL_STATE, NOT_FINAL_STATE

##### main #####

##### init #####
# fic
print("Start !\n")
fic = fichier.read()
fichier.close()
print (fic)

NB_INITIAL_STATE,INITIAL_STATE,NB_FINAL_STATE,FINAL_STATE,NB_TRANSITIONS,TRANSITIONS,ETATS,LIBELLES = lire_automate_sur_fichier(fic)
print('\n')

##### body #####
print("STANDARD:", est_un_automate_standard())
standardisation()
print("STANDARD APRÈS STANDARDISATION: ", est_un_automate_standard())
#afficher_automate()

print(est_un_automate_assynchrone())

if ASYNCHRONES: # elimination_epsilon
    elimination_epsilon()

'''
completion()

print(FINAL_STATE)
automate_complementaire()
print(FINAL_STATE)
'''
# determinisation_synchrone()

ecriture_automate_sur_fichier()
print("\n\nVIE !!!!!!!!!!!\ninit: ", NB_INITIAL_STATE,"\n",INITIAL_STATE,"\nfinal: ",NB_FINAL_STATE,"\n",FINAL_STATE,"\ntransit: ",NB_TRANSITIONS,"\n",TRANSITIONS,"\nasynchrone: ",ASYNCHRONES,"\n")

# determinisation_et_completion_asynchrone :
#   elimination epsilon puis deter/complet synchrone

# determinisation et completion synchrone :

