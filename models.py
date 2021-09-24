# importation des librairies

import pandas as pd
import numpy as np
import os
import glob
from lxml import etree
import xml.etree.ElementTree as et
import xmltodict
import re


class Book():

    def __init__(self, title: str, goodreads_book_id: int ,authors:list=[], book_id:int=0, books_count: int=0, 
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



class to_read():
    def __init__(self, user_id: int, book_id: int):
        self._user_id=int(user_id)
        self._book_id=int(book_id)



# ces classes ont à utiliser si un ORM est employé.
"""
class Book():

    def __init__(db.Model):

                __tablename__="house"
                authors=db.Column("authors", db.String(), nullable=True)
                id=db.Column('book_id', db.Integer(10), primary_key=True)
                books_count=db.Columns('books_count', db.Integer(15), nullable=True)
                original_title=db.Column('original_title', db.String(), nullable=True)
                language_code=db.Column('language_code', db.Integer(15), nullable=False )
                ratings_count=db.Column('ratings_count', db.Integer(15), nullable=True)
                goodreads_book_id=db.Column('goodreads_book_id', db.Integer(15), nullable=True)
                original_publication_year=db.Column('original_publication_year', db.Integer(15), nullable=True)
                rating1=db.Column('rating1', db.Integer(15), nullable=True)
                rating2=db.Column('rating2', db.Integer(15), nullable=True)
                rating3=db.Column('rating3', db.Integer(15), nullable=True)
                rating4=db.Column('rating4', db.Integer(15), nullable=True)
                rating5=db.Column('rating5', db.Integer(15), nullable=True)
                books_to_read=db.relationship('To_read', backref='Book', lazy=True)
                books_ratings=db.relationship('Rating', backref='Book', lazy=True)
                books_tags=db.relationschip('Book_tags', backref='Book', lazy=True )

    
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




class User():
    def __init__(db.Model):
        __tablename__ ='user'
        id=db.Column("user_id", db.Integer(15), primary_key=True)
        name=db.Column('user_name', db.String(), nullable=False)
        password=db.Column('password', db.String(15), nullable=False)
        user_rating=db.relationship('Rating', backref='user', lazy=True)
        user_to_read=db.relationship('To_read', backref='user', lazy=True)


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





class Tag():
    def __init__( db.Model ):
        __tablename__='tag'
        id=db.Column('tag_id', db.Integer(15), primary_key=True)
        title=db.Column('tag_title', db.String() , nullable=False)
        book_semantic=db.relationship('Book_tags', backref='tag', lazy=True)

    def insert_from_pd(data_tags: DataFrame):
        data_tags = data_tags.rename(
            columns={
                "id": "id",
                "title": "title"
                    }
                                        )
                                        
        data_tags.index += 1
        data_tags.to_sql("tags", if_exists="append", con=db.engine, index=False) 




class Rating():
    def __init__(db.Model):
        __tablename__='rating'
        id=db.Column('user_id', db.Integer() ,primary_key=True )
        book_id=db.Column('book_id', db.ForeignKey('book.id'), primary_key=True)
        rate=db.Column('rate', db.Integer(), db.ForeignKey('user.id') , nullable=False)

    def insert_from_pd(data_tags: DataFrame):
        data_tags = data_tags.rename(
            columns={
                "id": "id",
                "book_id": "book_id"
                    }
                                        )
                                        
        data_tags.index += 1
        data_tags.to_sql("ratings", if_exists="append", con=db.engine, index=False)     



class Book_tags():
    def __init__(db.Model):
        __tablename__='book_tags'
        goodreads_book_id=db.Column('goodreads_book_id', db.ForeignKey('book.goodreads_book_id'), db.Integer(15), primary_key=True)
        tag_id=db.Column('tag_id', db.Integer(15), db.ForeignKey('tag.id'), primary_key=True)
        count=db.Column('count', db.Integer(15), nullable=False)

    def insert_from_pd(data_book_tags: DataFrame):
        data_book_tags = data_book_tags.rename(
            columns={
                "goodreads_book_id": "goodreads_book_id",
                "tag_id": "tag_id"
                    }
                                        )
                                        
        data_book_tags.index += 1
        data_book_tags.to_sql("book_tags", if_exists="append", con=db.engine, index=False)

    
"""