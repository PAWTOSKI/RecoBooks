# importation des librairies

import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import enum
import os
import glob
from lxml import etree
import xml.etree.ElementTree as et
import xmltodict
import re
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, update
from sqlalchemy.orm import relationship
from database import Base, engine, DBsession

# ces classes sont définis selon le schéma imposé par l'ORM.

# Classe d'objet : livre

class Book(Base):

    #définition des arguments de la table
    __tablename__="books"
    __table_args__ = {'extend_existing': True}
    
    #définition desclonnes de la table
    authors=Column(String, nullable=True)
    title=Column(String, nullable=False)
    book_id=Column(Integer, primary_key=True)
    isbn=Column(String, nullable=True)
    books_count=Column(Integer, nullable=True)
    original_title=Column(String, nullable=True)
    language_code=Column(String, nullable=False )
    ratings_count=Column(Integer, nullable=True)
    goodreads_book_id=Column(Integer, nullable=True)
    original_publication_year=Column(Integer, nullable=True)
    ratings_1=Column(Integer, nullable=True)
    ratings_2=Column(Integer, nullable=True)
    ratings_3=Column(Integer, nullable=True)
    ratings_4=Column(Integer, nullable=True)
    ratings_5=Column(Integer, nullable=True)

    
    def __init__(self, title, goodreads_book_id,isbn, authors, book_id, books_count, 
                 original_title, language_code, ratings_count, original_publication_year, 
                 ratings_1: int=0, ratings_2: int=0, ratings_3: int=0, ratings_4: int=0, ratings_5: int=0 ):

                self.title=re.sub(r'(:?\W+)',' ', title).lower()
                self.authors=[re.sub(r'(:?\W+)', 
                                        i, 
                                        title)\
                                    .lower() for i in authors if isinstance(i,str)
                                ]

                self.book_id=book_id
                self.isbn=isbn
                self.books_count=books_count
                self.original_title=re.sub(r'(:?\W+)',' ', original_title).lower()
                self.language_code=language_code
                self.ratings_count=ratings_count
                self.goodreads_book_id=goodreads_book_id
                self.original_publication_year=int(original_publication_year)
                self.ratings_1=int(ratings_1)
                self.ratings_2=int(ratings_2)
                self.ratings_3=int(ratings_3)
                self.ratings_4=int(ratings_4)
                self.ratings_5=int(ratings_5)
    
    
    def insert_from_pd(data_books: DataFrame, db, n=10000):

        for chunk in range(0, data_books.shape[0]-1, 1000):
            db.bulk_insert_mappings(
                Book,
                [
                    dict(book_id=int(data_books.iloc[i]["book_id"]), authors=data_books.iloc[i]["authors"], books_count=int(data_books.iloc[i]["books_count"]),                        
                    original_title=data_books.iloc[i]["original_title"], language_code=data_books.iloc[i]["language_code"], 
                    ratings_count=int(data_books.iloc[i]["ratings_count"]), goodreads_book_id=int(data_books.iloc[i]["goodreads_book_id"]),  
                    original_publication_year= int(data_books.iloc[i]["original_publication_year"]), 
                    ratings_1=int(data_books.iloc[i]["ratings_1"]), ratings_2=int(data_books.iloc[i]["ratings_2"]), ratings_3=int(data_books.iloc[i]["ratings_3"]), 
                    ratings_4=int(data_books.iloc[i]["ratings_4"]), ratings_5=int(data_books.iloc[i]["ratings_5"]))
                    for i in range(chunk, min(chunk + 1000, data_books.shape[0]-1))
                ]
            )
        db.commit()
   

    # Extraction des livres similaires pour un livre donné sur la base de l'identifiant "goodreads_book_id",
    # ce à partir du fichier XML lui étant attribué.
    def get_similar_book(self):
        list_similar_b=[]

        #changement du répertoire de travail

        os.chdir("../RecoBooks")


        #extraction du chemin relatif vers la fiche du livre

        for file in glob.iglob(f'{os.getcwd()}/**/data/books_xml', recursive=True):
            root_file_book=file
        url_books_similar=f'{root_file_book}/{self.goodreads_book_id}.xml'


        #ouverture et parsage du fichier xml

        with open(url_books_similar, encoding="utf-8") as corpus:
            tree=et.parse(corpus)
            root=tree.getroot()
            xml_file=et.tostring(root).decode()


        # extraction des id des livres similaires

            for book_similar in xmltodict.parse(xml_file )['GoodreadsResponse']['book']['similar_books']['book'] : 
                print(book_similar['id'])
                list_similar_b.append(book_similar['id'])
        
        self.similar_books=list_similar_b


# Classe d'objet : utilisateur
class User(Base):
    
    #définition des arguments de la table

    __tablename__ ='users'
    __table_args__ = {'extend_existing': True} 
    user_id=Column(Integer(), primary_key=True)
    pseudo=Column(String(), nullable=False)
    password=Column(String(), nullable=False)


    def __init__(self, user_id, pseudo, password):
        self.user_id=user_id
        self.pseudo=pseudo
        self.password=password       


    def insert_from_pd(data_users: DataFrame):
        data_users.to_sql("users", if_exists="append", con=engine, index=False)


        

# Classe d'objet : Tag
class Tag(Base):
    
    #définition des arguments de la table

    __tablename__='tags'
    __table_args__ = {'extend_existing': True} 

    tag_id=Column(Integer, primary_key=True)
    tag_name=Column(String , nullable=False)
    

    def __init__( self, tag_id , tag_name):
        self.tag_id=tag_id
        self.tag_name=tag_name
        
        
    def insert_from_pd(data_tags: DataFrame):
        data_tags.to_sql("tags", if_exists="append", con=engine, index=False)


# Classe d'objet : Notes des avis
class Rating(Base):
    
    #définition des arguments de la table

    __tablename__='ratings'
    __table_args__ = {'extend_existing': True}

    user_id=Column(ForeignKey('users.user_id'), primary_key=True)
    book_id=Column(ForeignKey('books.book_id'), primary_key=True)
    rating=Column(Integer )

    #définition des relations clés primaires - clés étrangères, avec définition des modifications en cascade
    
    book=relationship('Book', cascade="save-update, delete", backref='ratings', 
                        innerjoin=True, lazy="joined")
    user=relationship('User', cascade="save-update, delete", backref='ratings', 
                        innerjoin=True, lazy="joined")

    def __init__(self, user, book, rating ):
        self.user_id=user
        self.book_id=book
        self.rating=rating    
        
       
    def insert_from_pd(data_ratings: DataFrame):
        data_ratings.to_sql("ratings", if_exists="append", con=engine, index=False)     



# Classe d'objet : catégories de livre
class Book_tags(Base):
    
    #définition des arguments de la table
    __tablename__='book_tags'
    __table_args__ = {'extend_existing': True} 

    goodreads_book_id=Column(ForeignKey("books.goodreads_book_id"), primary_key=True)
    tags_id=Column(ForeignKey("tags.tag_id"), primary_key=True)
    count=Column(Integer(), nullable=False)

    goodreads_book=relationship('Book', cascade="save-update, delete", backref='book_tags',
                        innerjoin=True, lazy="joined")
    tag=relationship('Tag', cascade="save-update, delete", backref='book_tags', 
                        innerjoin=True, lazy="joined")


    def __init__(self, goodreads_book, tag, count ):

        self.goodreads_book_id=goodreads_book
        self.tags_id=tag
        self.count=count
        

    def insert_from_pd(data_book_tags: DataFrame):
        data_book_tags.to_sql("book_tags", if_exists="append", con=engine, index=False)
       


## Classe d'objet : Livres prévus pour être lu par le lecteur
class To_read(Base):

    #définition des arguments de la table
    __tablename__='to_read'
    __table_args__ = {'extend_existing': True}

    user_id=Column( ForeignKey("users.user_id"), primary_key=True)
    book_id=Column( ForeignKey("books.book_id"), primary_key=True)

    #définition des relations clés primaires - clés étrangères, avec définition des modifications en cascade
    books=relationship("Book", cascade="save-update, delete", backref='to_read', 
                        innerjoin=True, lazy="joined")  
    users=relationship("User", cascade="save-update, delete", backref='to_read', 
                        innerjoin=True, lazy="joined")  
    
    def __init__(self, users, books):

        self.user_id=users
        self.book_id=books

        
    def insert_from_pd(data_to_reads: DataFrame):

        data_to_reads.to_sql('to_reads', con=engine, if_exists="append", index=False)