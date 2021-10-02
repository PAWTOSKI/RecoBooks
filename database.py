## coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

"""
        Ce script se permet d'établir une connexion à la base de données. 
        Il est utilisé les infos de connexion enregistré dans le config.json.
"""

with open('config.json', 'r') as fichier:
        data = json.load(fichier)
#recuperer les informations de connection à DB étant stocké dans fichir json

#choix = int(input("Choisissez un DB: Postgresql(0)/mysql(1) : "))
#if choix==0 :
#    data = listEngine[0]['info']
#elif choix == 1:
#    data = listEngine[1]['info']

db_info_connect = data["connector"]+"://"+data['user']+":"+data['pwd']+"@"+data['host']+':'+data['port']+'/'+data['bd']

engine = create_engine(db_info_connect, echo=True, future=True)

DBsession = sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine)

#declarer classe Base: contains a MetaData object where newly defined Table objects are collected
Base = declarative_base()

#Base.query = db_session.query_property()

"""from sqlalchemy import create_engine  
from sqlalchemy.orm import scoped_session, sessionmaker
import json
 
from sqlalchemy.ext.declarative import declarative_base

def getEngine():
    print('Charger le fichier config d\'engine de DB')
    with open('config.json', 'r') as fichier:
        data = json.load(fichier)

    db_info_connect = data["connector"]+"://"+data['user']+":"+data['pwd']+"@"+data['host']+':'+data['port']+'/'+data['bd']
    engine = create_engine(db_info_connect, echo=True, future=True)
    print('L\'engine est pret')
    return engine

engine=getEngine()


db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))
Base= declarative_base()"""
