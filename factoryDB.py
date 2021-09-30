import pandas as pd
import models
from database import engine, DBsession
from services import (format_tags_booktag, format_books, format_ratings, format_to_read, format_users)
from models import *

db_session = DBsession()

#models.Base.metadata.create_all(engine)
#DBsession.remove(db_session)


def insert_db():
    """
        Insère les données à la base de donnees
    """
    
    # On récupère les données du fichier CSV dans un dataframe; ajout de chemin RecoBooks/ si il ne marche pas
    print("Read CSV")
    books = pd.read_csv("data/books.csv")
#ratings = pd.read_csv("data/ratings.csv")
#to_reads = pd.read_csv("data/to_read.csv")
    tags = pd.read_csv("data/tags.csv", encoding="UTF-8")
    book_tags = pd.read_csv("data/book_tags.csv")
    #genres = creer_genre()

    #On formater, nettoyer des donnees
    print("Nettoyer data")
    books = format_books(books)
# data_users = format_users(ratings)
# ratings = format_ratings(ratings)

    #merger avec books afins d'avoir des ratings concernant des livres existants
#    data_ratings = pd.merge( books, ratings, validate="1:m", on="book_id")
#    data_ratings = data_ratings[ratings.columns].copy()
#    data_ratings = pd.merge(data_users, data_ratings, on="user_id", validate="1:m")
#    data_ratings = data_ratings[ratings.columns].copy()
    
    #affiner des tags, book_tags correspondant les livres exists
    data_tags, data_book_tags = format_tags_booktag(tags, book_tags)
    data_book_tags = pd.merge(books[['goodreads_book_id']], data_book_tags, on='goodreads_book_id' )
    
 #   to_reads = format_to_read(to_reads)
    #merger avec books afins d'avoir des book_to_read lié avec des livres existants
 #   data_toread = pd.merge( books, to_reads, validate="1:m", on="book_id")
 #   data_toread = data_toread[to_reads.columns].copy()
 #   data_toread = pd.merge(data_users, data_toread, on="user_id", validate="1:m")
 #   data_toread = data_toread[to_reads.columns].copy()
   

    #inserer les datas à BD
    print("Inserer data...")
    #Genre.insert_from_pd(genres, db_session)
 #   Book.insert_from_pd(books, db_session)
 #   User.insert_from_pd(data_users, db_session)
 #   Rating.insert_from_pd(data_ratings, db_session)
    Tag.insert_from_pd(data_tags, db_session)
    Book_tags.insert_from_pd(data_book_tags,db_session)
  #  To_read.insert_from_pd(data_toread, db_session)
 
    print("Les données sont insérées to DB")
 
    db_session.commit()
    
insert_db()