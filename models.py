# importation des librairies

import pandas as pd
import numpy as np
import os
import glob
from lxml import etree
import xml.etree.ElementTree as et
import xmltodict
import re

# ces classes ont à utiliser si un ORM est employé.


##Classe d'objet : livre

class Book(Base):



    __tablename__="house"
    authors=Column("authors", String(), nullable=True)
    id=Column('book_id', Integer(10), primary_key=True)
    books_count=Columns('books_count', Integer(15), nullable=True)
    original_title=Column('original_title', String(), nullable=True)
    language_code=Column('language_code', Integer(15), nullable=False )
    ratings_count=Column('ratings_count', Integer(15), nullable=True)
    goodreads_book_id=Column('goodreads_book_id', Integer(15), nullable=True)
    original_publication_year=Column('original_publication_year', Integer(15), nullable=True)
    rating1=Column('rating1', Integer(15), nullable=True)
    rating2=Column('rating2', Integer(15), nullable=True)
    rating3=Column('rating3', Integer(15), nullable=True)
    rating4=Column('rating4', Integer(15), nullable=True)
    rating5=Column('rating5', Integer(15), nullable=True)
    books_to_read=relationship('To_read', cascade="save-update, delete, delete-orphan") 
    books_tags=relationschip('Book_tags', cascade="save-update, delete, delete-orphan")

    
    """def __init__(self, title: str, goodreads_book_id: int ,authors:list=[], book_id:int=0, books_count: int=0, 
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
                self._rating5=int(rating5)"""
    
    
    def get_similar_book(goodreads_book_id):

        list_similar_b=[]

        #changement du répertoire de travail

        os.chdir("../RecoBooks")
        #extraction du chemin relatif vers la fiche du livre
        for file in glob.iglob(f'{os.getcwd()}/**/data/books_xml', recursive=True):
            root_file_book=file

        url_books_similar=f'{root_file_book}/{goodreads_book_id}.xml'


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


    def insert_from_pd(data_books: DataFrame):
        data_books = data_books.rename(
            columns={
                "authors": "authors",
                "book_id": "book_id",
                "books_count": "books_count",
                "original_title": "original_title",
                "language_code": "language_code",
                "ratings_count": "ratings_count",
                "goodreads_book_id": "goodreads_book_id",
                "original_publication_year": "original_publication_year",
                "rating1":"rating1", 
                "rating2":"rating2",
                "rating3":"rating3",
                "rating4":"rating4",
                "rating5":"rating5"    
                    }
                                        )
                                        
        data_books.index += 1
        data_books.to_sql("book", if_exists="append", con=db.engine, index=False)




class User(Base):
    
    __tablename__ ='user'
    id=Column("user_id", Integer(15), primary_key=True)
    name=Column('user_name', String(), nullable=False)
    password=Column('password', String(15), nullable=False)


    """def __init__(self, id: int, user_name: str, password: str):
        self._id=id
        self._user_name=str(user_name)
        self._password=str(password)"""
       

    def insert_from_pd(data_users: DataFrame):
        data_users = data_users.rename(
            columns={
                "id": "id",
                "name": "name", 
                "password":"password"
                    }
                                        )
                                        
        data_users.index += 1
        data_users.to_sql("user", if_exists="append", con=db.engine, index=False)        





class Tag(Base):
    
    __tablename__='tag'
    id=Column('tag_id', Integer(15), primary_key=True)
    title=Column('tag_title', String() , nullable=False)

    """def __init__( self, tag_id: str=='0', tag_title: str=='None' ):
        self._tag_id=tag_id
        self._tag_title=re.sub(r'(:?\W+)',' ', tag_title).lower()"""
    
    def insert_from_pd(data_tags: DataFrame):
        data_tags = data_tags.rename(
            columns={
                "id": "id",
                "title": "title"
                    }
                                        )
                                        
        data_tags.index += 1
        data_tags.to_sql("tags", if_exists="append", con=db.engine, index=False) 




class Rating(Base):
    
    __tablename__='rating'
    user_id=Column('user_id', ForeignKey('user.id'))
    book_id=Column('book_id', ForeignKey('book.id'))
    rate=Column('rate', Enum(1, 2, 3, 4, 5) )
    book=relationship('Book', cascade="save-update, delete, delete-orphan")
    user=relationship('User', cascade="save-update, delete, delete-orphan")

    """def __init__(self,  user_id: int=0, book_id: int=0, rate: int=0 ):
        self._user_id=user_id
        self._book_id=book_id
        self._rate=int(rate)"""

    def insert_from_pd(data_tags: DataFrame):
        data_tags = data_tags.rename(
            columns={
                "id": "id",
                "book_id": "book_id", 
                "rate": "rate"
                    }
                                        )
                                        
        data_tags.index += 1
        data_tags.to_sql("ratings", if_exists="append", con=db.engine, index=False)     



class Book_tags(Base):
    
    __tablename__='book_tags'
    goodreads_book_id=Column('book', ForeignKey("book.goodreads_book_id"))
    tag_id=Column('Tag', ForeignKey("tag.id"))
    count=Column('count', Integer(15), nullable=False)
    goodreads_book=relationship('Book', cascade="save-update, delete, delete-orphan")
    tag=relationship('Tag', cascade="save-update, delete, delete-orphan")


    """def __init__(self, goodreads_book_id: int=0, tag_id: int=0, count: int=0 ):

        self._goodreads_book_id=int(goodreads_book_id)
        self._tag_id=int(tag_id)
        self._count=int(count)"""


    def insert_from_pd(data_book_tags: DataFrame):
        data_book_tags = data_book_tags.rename(
            columns={
                "goodreads_book_id": "goodreads_book_id",
                "tag_id": "tag_id",
                "count": "count"
                    }
                                        )

        data_book_tags.index += 1
        data_book_tags.to_sql("book_tags", if_exists="append", con=db.engine, index=False)


class to_read(Base):
    
    user_id=Column("user_id", ForeignKey("user.id"))
    book_id=Column("book_id", ForeignKey("book.id"))
    books=relationship("Book", cascade="save-update, delete, delete-orphan")  
    users=relationship("User", cascade="save-update, delete, delete-orphan")  
    
