#from utils_db import *
import os
from os import system, name
import pandas as pd
from models import *
from sysRecomPopularite import PoPRecommend

global ratings, books 

def process_data(data):
    print("Beginning data processing...")
    modified_data = data + " that has been modified"
    
    print("Data processing finished.")
    return modified_data

def read_dataset_from_web():
    #recupérer le chemin de dossier courant
    dossier_courant = os.getcwd()
    pathDir = dossier_courant+"/"+"data"
    if str(os.path.exists((pathDir))) :
        print("Dossier est exist!")
    else :
        os.mkdir(pathDir)
    print("Reading data from the Web")
    data = "Data from the web"
    return data

def write_data_to_database(data):
    print("Writing data to a database")
    print(data)

def read_data_from_DB(ratings, books):
    ratings = pd.read_csv('data/ratings.csv')
    books = pd.read_csv('data/books.csv')
    return ratings, books

def print_result(lsResult: pd.DataFrame):
    cols = lsResult.columns
    
    for row in lsResult.shape[0]:
        print("Livre %d" %(row+1))
        print(lsResult[c]+"\t" for c in cols )
        print("---")

def menu() :
    print(("\tBienvenue de systeme de recommendation").upper())
    print("%30s" %("Recobook".upper()))
    print("%15s" %("Groupe: Souad - Wilried - Nga"))
    print("\n")
    ansUser = input("Vous êtes nouveau utilisateur (Yes-Oui/No-Non) : ")
    if (str(ansUser).lower() == "oui") | (str(ansUser).lower() == "yes") | (str(ansUser).lower() == "o"):
        print("Quel genre de livre préférez-vous (maximum: 5 genres) ?")
        print("Par example: action, fiction, adult, romance, science, fantasy, classic, comtemporary,...")
        list_genre_nv_user = input("Les genres sont séparés par ',' (appyez ENTRER pour terminer) : ")
        list_genre_nv_user = list_genre_nv_user.split(",")
        print("nb_genre = ", len(list_genre_nv_user))
        ratings = pd.read_csv('data/ratings.csv')
        books = pd.read_csv('data/books.csv')

        try:
            nombre_livre_recom = input("Combien de livre voulez-vous recommender ?")
        except ValueError:
            print("Il faut saisir un nombre (5, 10, 15, 16,...) ")
       
        popRecom = PoPRecommend(ratings, books)
        if (len(list_genre_nv_user)==1) & (str(list_genre_nv_user[0])==''):
            list_livre = popRecom.populariteNotePonderer(nombre_livre_recom)
            print()
            print("result = ", list_livre.shape )
            print("%15s" %("<<<< RESULTAT >>>>"))
            print_result(list_livre)
        else :
            print("System popolarite avec genre")
    else:
        
        try:
            identity = int(input("Votre identifiant: "))
        except ValueError:
            print("Désolé l'identifiant saisie n'est pas un nombre.")
        
        passwd = input("Mot de password (null): ") 

        #check identifiant à la base de données
        db_user_id, db_passwd = get_db(User.user_id , User.password)

        if (db_user_id==identity) & (db_passwd==db_passwd):
            print("systeme filtrage collaboratif")
        else:
            print("Identifiant est pas ")


def clear_screen():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def main():
    data = read_dataset_from_web()
    modified_data = process_data(data)
    write_data_to_database(modified_data)
    clear_screen()
    #ratings, books = read_data_from_DB(ratings, books)
    cont = True
    while cont :
        menu()
        tmp_cont = input("Voulez-vous continuer ? (O/N)")
        if (tmp_cont.lower() != "o") & (tmp_cont.lower() != "oui"):
            cont = False
        clear_screen()
    

if __name__ == "__main__":
    main()














