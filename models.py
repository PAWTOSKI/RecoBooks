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
                    dict(title=data_books.iloc[i]["title"],
                    goodreads_book_id=int(data_books.iloc[i]["goodreads_book_id"]),
                    isbn=data_books.iloc[i]["isbn"], 
                    authors=data_books.iloc[i]["authors"],
                    book_id=int(data_books.iloc[i]["book_id"]), 
                    books_count=int(data_books.iloc[i]["books_count"]), 
                    original_title=data_books.iloc[i]["original_title"], 
                    language_code=data_books.iloc[i]["language_code"], 
                    ratings_count=int(data_books.iloc[i]["ratings_count"]),   
                    original_publication_year=int(data_books.iloc[i]["original_publication_year"]), 
                    ratings_1=int(data_books.iloc[i]["ratings_1"]), 
                    ratings_2=int(data_books.iloc[i]["ratings_2"]), 
                    ratings_3=int(data_books.iloc[i]["ratings_3"]), 
                    ratings_4=int(data_books.iloc[i]["ratings_4"]), 
                    ratings_5=int(data_books.iloc[i]["ratings_5"]))
                    for i in range(chunk, min(chunk + 1000, data_books.shape[0]))
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


    def insert_from_pd(data_users: DataFrame, db, n=100000 ):
        for chunk in range(0, data_users.shape[0]-1, 10000):
            db.bulk_insert_mappings(
                User, [dict(
                    user_id=int(data_users.iloc[i]["user_id"]),
                    pseudo="pseudo",
                    password="" )  for i in range(chunk, min(chunk + 10000, data_users.shape[0]))
                ])
        db.commit()



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
        
        
    def insert_from_pd(data_tags: DataFrame, db, n=100000):
        for chunk in range(0, data_tags.shape[0]-1, 10000):
            db.bulk_insert_mappings(
                Tag, [dict(
                    tag_id=int(data_tags.iloc[i]["new_tag_id"]),
                    tag_name=data_tags.iloc[i]["tag_name"])
                    for i in range(chunk, min(chunk + 10000, data_tags.shape[0]))
                ])
        db.commit()


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
        
    
    def insert_from_pd(data_ratings: DataFrame, db, n=10000000):
        for chunk in range(0, data_ratings.shape[0]-1, 500000):
            db.bulk_insert_mappings(
                Rating, [dict(
                    user_id=int(data_ratings.iloc[i]["user_id"]),
                    book_id=int(data_ratings.iloc[i]["book_id"]),
                    rating=int(data_ratings.iloc[i]["rating"])) 
                    for i in range(chunk, min(chunk + 500000, data_ratings.shape[0]))
                ])
        db.commit()



# Classe d'objet : catégories de livre
class Book_tags(Base):
    
    #définition des arguments de la table
    __tablename__='book_tags'
    __table_args__ = {'extend_existing': True} 

    goodreads_book_id=Column('book', ForeignKey("books.goodreads_book_id"), primary_key=True)
    tag_id=Column(ForeignKey("tags.tag_id"), primary_key=True)
    count=Column(Integer(), nullable=False)
    goodreads_book=relationship('Book', cascade="save-update, delete", backref='book_tags')
    tag=relationship('Tag', cascade="save-update, delete", backref='book_tags')


    def __init__(self, goodreads_book_id, tag_id, count ):

        self._goodreads_book_id=goodreads_book_id
        self._tag_id=tag_id
        self._count=count
        

    def insert_from_pd(data_book_tags: DataFrame, db, n=1000000 ):
        for chunk in range(0, data_book_tags.shape[0]-1, 100000):
            db.bulk_insert_mappings(
                Book_tags, [dict(
                    goodreads_book_id=int(data_book_tags.iloc[i]["goodreads_book_id"]),
                    tag_id=int(data_book_tags.iloc[i]["new_tag_id"]),
                    count=int(data_book_tags.iloc[i]["count_x"])) 
                    for i in range(chunk, min(chunk + 100000, data_book_tags.shape[0]))
                ])
        db.commit()
    


## Classe d'objet : Livres prévus pour être lu par le lecteur
class To_read(Base):

    #définition des arguments de la table
    __tablename__='to_read'
    __table_args__ = {'extend_existing': True}

    user_id=Column("user_id", ForeignKey("users.user_id"), primary_key=True)
    book_id=Column("book_id", ForeignKey("books.book_id"), primary_key=True)

    #définition des relations clés primaires - clés étrangères, avec définition des modifications en cascade
    books=relationship("Book", cascade="save-update, delete", backref='to_read')  
    users=relationship("User", cascade="save-update, delete", backref='to_read')  
    
    
    def __init__(self, user_id, book_id, count ):

        self.user_id=user_id
        self.book_id=book_id

        
    def insert_from_pd(data_to_reads: DataFrame, db, n=100000 ):
        for chunk in range(0, data_to_reads.shape[0]-1, 10000):
            db.bulk_insert_mappings(
                To_read, [dict(
                    user_id=int(data_to_reads.iloc[i]["user_id"]),
                    book_id=int(data_to_reads.iloc[i]["book_id"]))
                    for i in range(chunk, min(chunk + 10000, data_to_reads.shape[0]))
                ])
        db.commit()



"""
#fonction de books
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
        
        similar_books=list_similar_b



class Book(Base):

    def __init__(self, title: str, goodreads_book_id: int,authors:list=[], book_id:int=0, books_count: int=0, 
                 original_title: str='0', language_code: str='', ratings_count:int=0, original_publication_year: int=0, 
                 rating1: int=0, rating2: int=0, rating3: int=0, rating4: int=0, rating5: int=0 ):

                self._title=re.sub(r'(:?\W+)',' ', title).lower()
                self._authors=[re.sub(r'(:?\W+)', 
                                        i, 
                                        title)\
                                    .lower() for i in authors if isinstance(i,str)
                                ]

                self._book_id=book_id
                self._books_count=books_count
                self._original_title=re.sub(r'(:?\W+)',' ', original_title).lower()
                self._language_code=language_code
                self._ratings_count=ratings_count
                self._goodreads_book_id=goodreads_book_id
                self._original_publication_year=int(original_publication_year)
                self._rating1=int(rating1)
                self._rating2=int(rating2)
                self._rating3=int(rating3)
                self._rating4=int(rating4)
                self._rating5=int(rating5)

    def get_similar_book(self):

        list_similar_b=[]

        #changement du répertoire de travail

        os.chdir("../RecoBooks")
        #extraction du chemin relatif vers la fiche du livre
        for file in glob.iglob(f'{os.getcwd()}/**/data/books_xml', recursive=True):
            root_file_book=file

        url_books_similar=f'{root_file_book}/{self._goodreads_book_id}.xml'


        #ouverture et parsage du fichier xml

        with open(url_books_similar, encoding="utf-8") as corpus:
            tree=et.parse(corpus)
            root=tree.getroot()
            xml_file=et.tostring(root).decode()


        # extraction des id des livres similaires

            for book_similar in xmltodict.parse(xml_file )['GoodreadsResponse']['book']['similar_books']['book'] : 
                print(book_similar['id'])
                list_similar_b.append(book_similar['id'])
        
        self._similar_books=list_similar_b


class User():
    def __init__(self, id: int, user_name: str, password: str):
        self._id=id
        self._user_name=str(user_name)
        self._password=str(password)



class Tag():
    def __init__( self, tag_id: str=='0', tag_title: str=='None' ):
        self._tag_id=tag_id
        self._tag_title=re.sub(r'(:?\W+)',' ', tag_title).lower()



class Rating():
    def __init__(self,  user_id: int=0, book_id: int=0, rate: int=0 ):
        self._user_id=user_id
        self._book_id=book_id
        self._rate=int(rate)



class Book_tags():
    def __init__(self, goodreads_book_id: int=0, tag_id: int=0, count: int=0 ):

        self._goodreads_book_id=int(goodreads_book_id)
        self._tag_id=int(tag_id)
        self._count=int(count)



class To_read():
    def __init__(self, user_id: int, book_id: int):
        self._user_id=int(user_id)
        self._book_id=int(book_id)



# ces classes ont à utiliser si un ORM est employé.
"""

    
