# importation des librairies

import pandas as pd
import numpy as np
import os
import glob
from lxml import etree
import xml.etree.ElementTree as et
import xmltodict
import re
from pandas import DataFrame
from sqlalchemy import Column, Integer, String, ForeignKey, Table, BigInteger
from sqlalchemy.orm import relationship
from database import Base, engine #importer objet Base du fichier database.py



class Book(Base):
 
   #définition des arguments de la table
    __tablename__="books"
    __table_args__ = {'extend_existing': True}
    
    #définition desclonnes de la table
    authors=Column(String, nullable=True)
    title=Column(String, nullable=False)
    book_id=Column(Integer, primary_key=True)
    isbn=Column(Integer, nullable=True)
    books_count=Column(Integer, nullable=True)
    original_title=Column(String, nullable=True)
    language_code=Column( Integer, nullable=False )
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


class Tag(Base):
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String(200), nullable=False)
    
    book_semantic = relationship('Book_tag', backref='tags', lazy=True)


    def insert_from_pd(data_tags: DataFrame):
        data_tags.to_sql("tags", if_exists="append", con=engine, index=False) 


class User(Base):
    __tablename__ = 'users'
        
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False)
    password = Column(String(15), nullable=False)
    
    #set relationship
    user_rating = relationship('Rating', backref='users', lazy=True)
    user_to_read = relationship('To_read', backref='users', lazy=True)


    def insert_from_pd(data_users: DataFrame):
        data_users.to_sql("users", if_exists="append", con=engine, index=False)        



class Rating(Base):
    __tablename__ = 'ratings'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True )
    book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)
    rating = Column(Integer, nullable=False)


    def insert_from_pd(data_ratings: DataFrame):
        data_ratings.to_sql("ratings", if_exists="append", con=engine, index=False)     



class Book_tag(Base):
    __tablename__='book_tags'
    
    goodreads_book_id = Column(Integer, ForeignKey('books.goodreads_book_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key=True)
    count = Column(Integer, nullable=False)

    def insert_from_pd(data_book_tags: DataFrame):
        data_book_tags.to_sql("book_tags", if_exists="append", con=engine, index=False)



class To_read(Base):
    __tablename__ = 'to_reads'
    
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)


    def insert_from_pd(data_to_reads: DataFrame):

        data_to_reads.to_sql('to_reads', con=engine, if_exists="append", index=False)




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

    
