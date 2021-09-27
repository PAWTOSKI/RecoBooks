import pandas as pd
import model
from database import engine, DBsession
from services import (format_books, format_tags, format_ratings, format_to_read, format_book_tags)
from model import Book, Tag, Rating, Book_tags, To_read

db_session = DBsession()
model.Base.metadata.create_all(engine)


def insert_db():
    """
        Insère les données à la base de donnees
    """
    
    # On récupère les données du fichier CSV dans un dataframe
    print("Read CSV")
    books = pd.read_csv("RecoBooks/data/books.csv")
    ratings = pd.read_csv("RecoBooks/data/ratings.csv")
    to_reads = pd.read_csv("RecoBooks/data/to_read.csv")
    tags = pd.read_csv("RecoBooks/data/tags.csv", encoding="encoding='UTF-8")
    book_tags = pd.read_csv("RecoBooks/data/book_tags.csv")

    #On formater, nettoyer des donnees
    print("Nettoyer data")
    books = format_books(books)
    ratings = format_ratings(ratings)
    tags = format_tags(tags)
    book_tags = format_book_tags(tags, book_tags)
    #supprimer anciens tag_id du df tags
    tags = tags[['new_tag_id','tag_name']].copy() 
    tags = tags.rename(columns={'new_tag_id':'tag_id'})
    
    to_reads = format_to_read(to_reads)

    #inserer les datas à BD
    print("Inserer data...")
    Book.insert_from_pd(books)
    Tag.insert_from_pd(tags)
    Rating.insert_from_pd(ratings)
    Book_tags.insert_from_pd(book_tags)
    To_read.insert_from_pd(to_reads)
    print("Les données sont insérées to DB")
    db_session.commit()
    
insert_db()