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

global data_ratings, data_books , data_users, data_toread, data_tags, data_booktags

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
    insert_alldb()


def read_data_from_DB():
    global data_books, data_ratings, data_users, data_toread, data_tags, data_booktags

    col_book = [Book.book_id, Book.goodreads_book_id, Book.ratings_count, Book.isbn, Book.title, Book.original_title, Book.original_publication_year]
    col_name_book = ['book_id','goodreads_book_id', 'ratings_count', 'isbn', 'title', 'original_title', 'original_publication_year']
    col_rating = [Rating.book_id, Rating.user_id, Rating.rating]
    col_name_rating = ['book_id','user_id', 'rating']
    col_user = [User.user_id, User.password]
    col_name_user = ['user_id', 'password']
    col_tag = [Tag.tag_id, Tag.tag_name]
    col_name_tag = ['tag_id', 'tag_name']
    col_toread = [To_read.book_id, To_read.user_id]
    col_name_toread = ['book_id', 'user_id']
    col_booktag =[Book_tags.goodreads_book_id, Book_tags.tag_id, Book_tags.count]
    col_name_booktag =['goodreads_book_id', 'tag_id', 'count']
    
    data_books = pd.DataFrame(get_db(col_book), columns=col_name_book).reset_index()
    data_ratings = pd.DataFrame(get_db(col_rating), columns=col_name_rating).reset_index()
    data_tags = pd.DataFrame(get_db(col_tag), columns=col_name_tag).reset_index()
    data_users = pd.DataFrame(get_db(col_user), columns=col_name_user).reset_index
    data_toread = pd.DataFrame(get_db(col_toread), columns=col_name_toread).reset_index()
    data_booktags = pd.DataFrame(get_db(col_booktag), columns=col_name_booktag).reset_index()

    return data_ratings, data_books, data_users, data_toread, data_tags, data_booktags


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
        
        if list_genre_nv_user=="":
            list_genre_nv_user=[]
        else:
            list_genre_nv_user = list_genre_nv_user.split(",")
       
        try:
            nombre_livre_recom = int(input("Combien de livre voulez-vous recommender ?"))
        except ValueError:
            print("Il faut saisir un nombre (5, 10, 15, 16,...) ")
            nombre_livre_recom = int(input("Reessayez: "))
       
        if nombre_livre_recom == 0 : 
            nombre_livre_recom = 30

        if (len(list_genre_nv_user)==0) :
            list_livre = populariteNotePonderer(data_ratings[['book_id', 'user_id', 'rating']], nombre_livre_recom)
            print()

            print("%15s" %("<<<< RESULTAT >>>>"))
            list_livre = pd.merge(list_livre, data_books, on='book_id')
            
            print(list_livre[['book_id','score','isbn','original_publication_year','title','original_title']])
       
        else :
            print("---System popularite avec genre ---")

    else:
        
        try:
            identity = int(input("Votre identifiant: "))
        except ValueError:
            print("Désolé l'identifiant saisie n'est pas un nombre.")
            identity = int(input("eessayez: "))
        
        passwd = input("Mot de password (null): ") 

        #check identifiant à la base de données
        #check_user = data_users[(int(data_users['user_id'])==identity) & (data_users['password']==passwd)]
        #db_user_id, db_passwd = get_db(User.user_id , User.password)
        
        #print('check = ', check_user)
        identity = 1234
        check_user = True
        if check_user:
            ma_ratings = matrixRating(data_ratings)
            mtrain, mtest = create_train_test(ma_ratings)
            als = ExplicitMF(n_iters = 20, n_factors = 40, reg = 0.01)
            als.fit(np.array(mtrain), np.array(mtest))
            
            book_recom = als.bookRecom(identity,als,data_books)
            print(book_recom)
        else:
            print("Identifiant n'existe pas ")


def clear_screen():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def main():
    global data_ratings, data_books , data_users, data_toread, data_tags, data_booktags

    print("Telecharger des données de URL...")
    #data = read_dataset_from_web()

    print("Creer DB et insérer les donnes pour l'application!")
    write_data_to_database()
    
    #charger des df pour application
    data_ratings, data_books, data_users, data_toread, data_tags, data_booktags = read_data_from_DB()

    cont = True
    while cont :
        menu()
        tmp_cont = input("Voulez-vous continuer ? (O/N)")
        if (tmp_cont.lower() != "o") & (tmp_cont.lower() != "oui"):
            cont = False
        clear_screen()
    

if __name__ == "__main__":
    main()














