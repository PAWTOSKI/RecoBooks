#from utils_db import *
import os
from os import system, name
import pandas as pd
from sqlalchemy import MetaData, Table, select
from models import *
from sysRecomPopularite import populariteNotePonderer
from factoryDB import *
from als import *
from utils_db import *
from database import engine

global data_ratings, data_books 

def process_data(data):
    print("Beginning data processing...")
    modified_data = data + " that has been modified"
    
    print("Data processing finished.")
    return modified_data

def read_dataset_from_web():
    #recupérer le chemin de dossier courant
    dossier_courant = os.getcwd()
    print(dossier_courant)
    pathDir = dossier_courant+"/"+"data"
    if str(os.path.exists((pathDir))) :
        print("Dossier est exist!")
    else :
        os.mkdir(pathDir)
        print("Reading data from the Web")
        print("creer tous les données alimentées pour app dans dossier data/")


def write_data_to_database():
    print("Creer une base de donnees à SGBD...")
    #create_db()
    print("Intégrer les données dans DB va commencer -->>>")
    #insert_db()


def read_data_from_DB():
    #metadata = MetaData()
    #con = engine.connect()
    #data_ratings = con.execute(select(Table('ratings', metadata, autoload=True, autoload_with=engine)))
    #data_books = con.execute(select(Table('books', metadata, autoload=True, autoload_with=engine)))
    global data_books, data_ratings

    data_books = read_table(Book)
    data_ratings = read_table(Rating)
    return data_ratings, data_books

#def print_result(lsResult: pd.DataFrame):
#    cols = lsResult.columns
#    print(cols)
#    
#    for row in range(lsResult.shape[0]):
#        print("Livre %d" %(row+1))
#        print(lsResult.iloc[row:row+1][c]+"\t" for c in cols )
#        print("---")


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
        
        try:
            nombre_livre_recom = int(input("Combien de livre voulez-vous recommender ?"))
        except ValueError:
            print("Il faut saisir un nombre (5, 10, 15, 16,...) ")
            nombre_livre_recom = int(input("Reessayez: "))
       
        if nombre_livre_recom == 0 : 
            nombre_livre_recom = 30
        if (len(list_genre_nv_user)==1) & (str(list_genre_nv_user[0])==''):
            list_livre = populariteNotePonderer(data_ratings, nombre_livre_recom)
            print()
            #print("result = ", list_livre.shape )
            print("%15s" %("<<<< RESULTAT >>>>"))
            print(list_livre)
        else :
            print("System popolarite avec genre")
    else:
        
        try:
            identity = int(input("Votre identifiant: "))
        except ValueError:
            print("Désolé l'identifiant saisie n'est pas un nombre.")
            identity = int(input("eessayez: "))
        
        passwd = input("Mot de password (null): ") 

        #check identifiant à la base de données
        db_user_id, db_passwd = get_db(User.user_id , User.password)
       
        #db_user_id = 1243
        #passwd = 0
        #db_passwd = ""
        #identity = 1243

        if (db_user_id==identity) & (db_passwd==passwd):
            mf_exp = ExplicitMF()
            book_recom = mf_exp.bookRecom(db_user_id,model,data_books)
            print(book_recom)
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
    global data_ratings, data_books 
    print("Creer DB et insérer les donnes pour l'application!")
    #data = read_dataset_from_web()
    #modified_data = process_data(data)
    #write_data_to_database()
    
    data_ratings, data_books = read_data_from_DB()
    print("ratings = ", data_ratings.shape)
    print("books = ", data_books.shape)
    cont = True
    while cont :
        menu()
        tmp_cont = input("Voulez-vous continuer ? (O/N)")
        if (tmp_cont.lower() != "o") & (tmp_cont.lower() != "oui"):
            cont = False
        clear_screen()
    

if __name__ == "__main__":
    main()














