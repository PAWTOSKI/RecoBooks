# importation des librairies dédiées à la gestion de la Base de données

from models import *
from sqlalchemy import update, text, select
from database import engine


#fonction d'insertion d'enregistrements au travers d'une transaction:

def insert_db(list_object):
        global DBsession
        with DBsession.begin() as session:
                session.add_all(list_object)

    #exemple: user1=User(1234, 'essai1', 'essai1')
    #           user2=User(1277, 'essai2', 'essai2' )
    #           insert_db([user1,user2])


#modification d'un enregistrement selon un ou plusieurs critères, via une transaction

def update_db(Table, params, condition ):
    global DBsession
    with DBsession.begin() as session:
        session.execute(Table.__table__.update().values(params).where(condition))
                            
    #exemple: update_db(User, {"pseudo":19199, "password":'essai_update1'} ,condition=(User.user_id>1235) & (User.pseudo!=19012))


#fonction de suppression des 

def delete_db(Table, condition ):

    global DBsession

    with DBsession.begin() as session:
        session.execute(Table.__table__.delete().where(condition))

    #exemple: delete_db(Rating, condition=(Rating.user_id>1235) )


#fonction de visionnage d'enregistements,  au travers d'une transaction:

def get_db( columns, list_key_on: dict={}):
    global DBsession
    
    with DBsession.begin() as session:
        if list_key_on=={}:
            statement=select(columns)
            view=session.execute(statement)
            
        elif isinstance(list_key_on, dict): 
            statement=select(columns)
            for table in list_key_on:
                statement=statement.join(table, list_key_on[table][0]==list_key_on[table][1])

            view=session.execute(statement)

    return view.all()

    #exemple: get_db(Book.book_id)



