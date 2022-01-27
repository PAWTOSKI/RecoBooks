import pandas as pd
import sqlalchemy as sql
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import seaborn as sns
import numpy as np
import configuration
import re

engine=configuration.connexion('simplion','Simplon2020','recobooks')

#lecture Dataset
def lecturedata (path,dataset):
    return pd.read_csv(path+"\\"+dataset, delimiter=',')

#supprimer les - des tags, les espaces vide, chiffres, les caracètes spéciaux,[old , toread, read, new]
def netoieTags (x):
    x=''.join(char.lower() for char in x if char.isalpha() and char!=' ')
    x=re.sub('(.+)(s)',r"\1",x) #supprimer les s à la fin 
    x=re.sub('[read,new,old,toread]','',x)
    return  x if len(x)>3  else '' #garder que les tags qui ont plus de 3caracteres


def insertionTags(tags, book_tags):
    tags['tag_name']=tags['tag_name'].apply(lambda x :netoieTags(x)) #appliquer le netoyage sur l'ensemble des lignes tags
    tags = tags.replace('', np.nan, regex=True) #remplacer les vide par nan pour
    tags=tags.dropna()
    tags=tags.reset_index(drop=True)
    new_tags=pd.DataFrame(list(tags['tag_name'].unique().tolist()),columns=['tag_name'])
    new_tags['new_tag_id']=new_tags.index+1
    tags=pd.merge(tags,new_tags, how='left',on='tag_name')
    
    #Actualiser count tags_id dans book_tags
    book_tags=pd.merge(book_tags,tags,how='left' ,on='tag_id')
    book_tags=book_tags.dropna()
    book_tags=book_tags.reset_index(drop=True)
    book_tags = book_tags.groupby(['goodreads_book_id','new_tag_id']).agg({'count':'sum'}).reset_index()
    book_tags.rename(columns={'new_tag_id':'tag_id'}, inplace=True)
    
    #insertion tags et book_tags dans BDD
    del tags['tag_id'] #supprimer anciens tag_id
    tags.rename(columns={'new_tag_id':'tag_id'})
    tags. to_sql('tags', if_exists='append', con=engine, index=False) #insertion dans tags
    book_tags.to_sql('book_tags',if_exists='append', con=engine,index=False)
    
    