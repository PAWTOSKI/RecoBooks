import pandas as pd
import model
import os
from database import engine, DBsession
from services import (format_books, format_tags, format_ratings, format_to_read, format_book_tags)
from model import Book, Tag, Rating, Book_tags, To_read



def create_database():
    """
        creer les tables dans un SGDB
    """
    models.Base.metadata.create_all(engine)
    db_session.commit()



def insert_db():
    """
        Insère les données à la base de donnees
    """
    
    # On récupère les données du fichier CSV dans un dataframe
    print("Read CSV")
    books = pd.read_csv("RecoBooks/data/books.csv")
    ratings = pd.read_csv("RecoBooks/data/ratings.csv")
    to_reads = pd.read_csv("RecoBooks/data/to_read.csv")
    tags = pd.read_csv("RecoBooks/data/tags.csv", encoding="UTF-8")
    book_tags = pd.read_csv("RecoBooks/data/book_tags.csv")

    #On formater, nettoyer des donnees
    print("---1. Nettoyer data")
    books = format_books(books)
    tags = format_tags(tags)
    to_reads = format_to_read(to_reads)
    ratings = format_ratings(ratings)
    book_tags = format_book_tags(book_tags)

    #inserer les datas à BD
    print("---2. Inserer data...")
    Book.insert_from_pd(books)
    Tag.insert_from_pd(tags)
    Rating.insert_from_pd(ratings)
    Book_tags.insert_from_pd(book_tags)
    To_read.insert_from_pd(to_reads)
    print("Les données sont insérées to DB")
    db_session.commit()


db_session = DBsession()    
#print("Creer des tables à la DB.... ")
#create_database()
print("Intégrer des donnees commence...")
insert_db()