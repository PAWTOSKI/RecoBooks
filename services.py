import pandas as pd
import numpy as np
import re



def format_books(data_books: pd.DataFrame):
    """
        nettoyer et formatter des données fournant par dataframe: books
        afin d'avoir un df books tout prête à insérer dans BD
        *** Params:
            data_books: dataframe étant chargé de fichier de données brutes
        *** Return:
            dataframe est prête d'inserer
    """
    #nettoyage et uniformisation des labels de titres originaux. En effet, il est a été adopter par convention par les
    # auteurs qu'une valeur manquante dans ce champ d'un film signifie que ce film n'a été publié qu'en une seule édition.
    # Par conséquent, le champ "Title" équivaut au champ "Original_title" dans ce cas de figure et il convient d'insérer dans
    # une valeur par défaut dans le champ "Original_title". 

    #suppresion des doubons
    data_books.drop_duplicates(inplace=True)
    
    mask=data_books["original_title"].isna()
    data_books.loc[mask,"original_title"]=='0'

    #suppresion des doubons
    data_books.dropna(inplace=True)

    ### preparer dataframe
    data_books = data_books[["book_id", "authors","title", "isbn", "books_count", "original_title", "language_code", "ratings_count", "goodreads_book_id", "original_publication_year", "ratings_1", "ratings_2", "ratings_3", "ratings_4", "ratings_5"]].copy()
    data_books = data_books.rename(
        columns = {
            "title": "title",
            "book_id": "book_id",
            "authors": "authors",
            "isbn": "isbn",
            "books_count": "books_count",
            "original_title": "original_title",
            "language_code": "language_code",
            "ratings_count": "ratings_count",
            "goodreads_book_id": "goodreads_book_id",
            "original_publication_year": "original_publication_year",
            "ratings_1":"ratings_1", 
            "ratings_2":"ratings_2",
            "ratings_3":"ratings_3",
            "ratings_4":"ratings_4",
            "ratings_5":"ratings_5"    
                }
        )
    data_books.index += 1
    
    return data_books



def format_ratings(data_ratings: pd.DataFrame):
    """
        afin d'avoir un df ratings tout prête à insérer dans BD
    """

    #suppresion des doubons
    data_ratings.drop_duplicates(inplace=True)

    #suppresion des doubons
    data_ratings.dropna(inplace=True)    

    data_ratings = data_ratings.rename(
            columns = {
                "user_id": "user_id",
                "book_id": "book_id",
                "rating": "rating"
                    }
        )
    data_ratings.index += 1
    
    return data_ratings


def format_users(data_ratings: pd.DataFrame):
     
    data_users = pd.DataFrame(data_ratings["user_id"].drop_duplicates(), columns=["user_id"])
    data_users = data_users.reset_index()
    data_users = data_users.drop('index', axis=1)
    data_users['pseudo'] = "pseudo"
    
    return data_users



def netoieTags (x):
    """
        Nettoyer les tags
        *** Params:
        x: tag_name
        *** Return
        tag_name nettoyé et normalisé
    """
    x = ''.join(char.lower() for char in x if char.isalpha() and char!=' ')
    
    #supprimer les s à la fin 
    x = re.sub('(.+)(s)',r"\1",x) 
    x = re.sub('[read,new,old,toread]','',x)
    
    #garder que les tags qui ont plus de 3 caracteres
    return  x if len(x)>3  else '' 



def format_tags(data_tags: pd.DataFrame):
    """
        préparer df tags afin d'avoir un df prête à insérer dans BD
    """
    # nettoyer tag_name au fonction de netoieTags
    data_tags['tag_name'] = data_tags['tag_name'].apply(lambda x :netoieTags(x)) #appliquer le netoyage sur l'ensemble des lignes tags
    
    #remplacer les vide par nan pour
    data_tags = data_tags.replace('', np.nan, regex=True) 
    data_tags = data_tags.dropna()
    data_tags = data_tags.reset_index(drop=True)

    #créer df new_tag de liste de tag_name étant nettoyés
    new_tags = pd.DataFrame(list(data_tags['tag_name'].unique().tolist()), columns=['tag_name'])
    new_tags['new_tag_id'] = new_tags.index+1
    data_tags = pd.merge(data_tags,new_tags, how='left',on='tag_name')
    
    data_tags = data_tags.rename(
        columns = {
            "id_tag": "id",
            "tag_name": "tag_name",
            "new_tag_id": "new_tag_id"
                }
        )
    data_tags.index += 1
    
    return data_tags



def format_book_tags(data_tags : pd.DataFrame, data_book_tags: pd.DataFrame):
    """
        nettoyer et formatter book_tags et Actualiser la valeur de count  
        afin d'avoir df book_tags prête à insérer dans BD
        
        *** Params:
        - data_tags : df de tags étant nettoyé
        - data_book_tags : df de book_tags lisant de fichier
        
        *** Return:
        df data_book_tags avec de nouveuau tag_id et count étant actualisé
    """
    
    data_book_tags = pd.merge(data_book_tags, data_tags, how='left' ,on='tag_id')
    
    #suppresion des doubons
    data_book_tags.drop_duplicates(inplace=True)
    #data_book_tags = data_book_tags.dropna(inplace=True)
    data_book_tags = data_book_tags.reset_index(drop=True)
    data_book_tags = data_book_tags.groupby(['goodreads_book_id','new_tag_id']).agg({'count':'sum'}).reset_index()
    data_book_tags.rename(columns={'new_tag_id':'tag_id'}, inplace=True)
    
    data_book_tags = data_book_tags.rename(
            columns = {
                "goodreads_book_id": "goodreads_book_id",
                "tag_id": "tag_id",
                "count": "count"
                    }
        )
    data_book_tags.index += 1
    
    return data_book_tags


def format_to_read(to_read: pd.DataFrame):
    """
        nettoyer et formatter des données de df to_read pour insérer dans BD
    """
    to_read.drop_duplicates(inplace=True)
    to_read.dropna(inplace=True)
    
    return to_read



def format_user(data_users: pd.DataFrame):
    """
        
    """
    #suppresion des doubons
    data_users.drop_duplicates(inplace=True)

    #suppresion des doubons
    data_users.dropna(inplace=True)  

    data_users = data_users.rename(
        columns={
            "user_id": "id",
            "name": "name", 
            "password":"password"
                }
        )
    data_users.index += 1        
    
    return data_users

########################## WIL

#    tags. to_sql('tags', if_exists='append', con=engine, index=False) #insertion dans tags
#    book_tags.to_sql('book_tags',if_exists='append', con=engine,index=False)
    
    
