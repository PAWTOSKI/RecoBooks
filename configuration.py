import sqlalchemy, pymysql
from sqlalchemy import create_engine


def connexion(user,pwd,bdd):
    return create_engine('mysql+pymysql://'+user+':'+pwd+'@localhost:3306/'+bdd)