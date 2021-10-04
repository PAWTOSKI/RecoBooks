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
    data_books = data_books.reset_index(drop=True)

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
    data_ratings = data_ratings.reset_index(drop=True)   

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



def format_tags_booktag(tags : pd.DataFrame, booktags: pd.DataFrame):
    """
        nettoyer et formatter book_tags et Actualiser la valeur de count  
        afin d'avoir df book_tags prête à insérer dans BD
        
        *** Params:
        - data_tags : df de tags étant nettoyé
        - data_book_tags : df de book_tags lisant de fichier
        
        *** Return:
        df data_book_tags avec de nouveuau tag_id et count étant actualisé
    """
    
    #calculer la totalité de nb fois taggé par tag -> affecter à occ_count
    occ_count=pd.DataFrame(booktags.groupby(['tag_id'])['count']
                    .agg('sum').sort_values( ascending = False ))
    #confusionner av tags afins d'avoir tag_name
    occ_count = pd.merge(occ_count, tags, on="tag_id")
    #convertir en minuscule et enlever des chars speciaux
    occ_count['tag_name'] = occ_count['tag_name'].apply(
            lambda x:''.join(char.lower() for char in x if char.isalpha() or char=='-')) 

    #supprimer les - au debut
    occ_count['tag_name'] = occ_count['tag_name'].apply(lambda x: re.sub('^-+(.+)',r"\1",x) )

     # definir les mots à supprimer
    listMot = [ "to-", "re-", "read-", "reading" "-in-", "-before-", "-die", 
                "you-", "must-", "-to-", "finish", "never", "finished", "finish-ed",
                "i-own", "owned", "buy", "-buy$", "bought", "-my-", "-it$", "own", 
                "did-not", "maybe", "borrrowed", "have", "to-have", "didn-t", "for", 
                "on-shelf", "-of-", "on-hold","-me-", "madecry", "need", "currently", 
                "-book", "-than-once", "challenge", "my-", "-reading", "-all-", "-and-",
                 "read", "^lol$", "-now-", "aa-", "about-"]

    #supprimer les tags inutiles
    for i in listMot : 
        occ_count['tag_name'] = occ_count['tag_name'].apply(lambda x: re.sub(i,"",x))
    
    #definir les tags devraient normaliser
    dic_mot_remplace = {    "-fi-": "-fiction", "-fi$": "-fiction",
                            "-fi(c)+-": "-fiction-", "non-fiction": "nonfiction",
                            "non-fic$": "nonfiction", "sci$": "science",
                            "sc(i)+-": "science-", "scifi": "science-fiction",
                            "y-a$":"young-adult", "ya-":"young-adult-",
                            "ya$":"young-adult", "youngadult":"young-adult",
                            "favourite": "favorite", "ｆａｖｏｒｉｔｅｓ": "favorite",
                            "cómic": "comic",
                            "clàssic": "classic", "mangá": "manga", 
                            "childhood": "children", "chick-lit": "chicklit",
                            "kids": "children", "kiddle": "children",
                            "vamp$": "vampire", "-lit$": "",
                            "literary": "literature", "families": "family",
                            "historical": "history", "humour": "humor", 
                            "romantic": "romance", "série": "serie",
                            "lgbtq": "lgbt", "religiou": "religion", 
                            "house": "home", "werewolve": "werewolf",
                            "youth": "young", "e-book": "ebook",
                            "audio-book": "audiobook", "(.+)ies" : r"\1y",
                            "fictionfantasy": "fiction-fantasy",
                            "sery": "serie", "engl$": "english", "eng$": "english",
                            "ｍａｎｇａ": "manga", "ｓｅｒｉｅｓ": "serie", 
                            "absolutely": "absolute"
                        }
    for k,v in dic_mot_remplace.items():
        occ_count['tag_name'] = occ_count['tag_name'].apply(lambda x: re.sub(k,v,x))
    
    #supprimer les - au debut
    occ_count['tag_name'] = occ_count['tag_name'].apply(lambda x: re.sub('^-*(.+)',r"\1",x) )
    occ_count['tag_name'] = occ_count['tag_name'].apply(lambda x: re.sub('-s$','', x))

    occ_count = occ_count.replace('-in-', np.nan, regex=True) 
    occ_count = occ_count.replace('^a-', np.nan, regex=True)
    occ_count = occ_count.replace('', np.nan, regex=True) 
    occ_count = occ_count.dropna()
    occ_count['tag_name'] = occ_count['tag_name'].apply(lambda x: re.sub('(.+)s$',r'\1',x) )
    
    occ_count['tag_name'] = occ_count['tag_name'].apply(lambda x: re.sub('(.+)-$',r'\1',x) )

    #enlève les tags dont sa longue est moins 3  
    occ_count['tag_name'] = occ_count['tag_name'].apply(lambda x: x if len(x)>=3 else '')
    occ_count['tag_name'] = occ_count['tag_name'].apply(lambda x: re.sub('^\S-\S$','', x))
        
    occ_count = occ_count.replace('', np.nan, regex=True) 
    occ_count = occ_count.dropna()
    #occ_count = occ_count.drop_duplicates().reset_index().rename(columns={'index':'new_tag_id'})
    occ_count_tagname = occ_count['tag_name'].drop_duplicates().reset_index().rename(columns={'index':'new_tag_id'})
    occ_count = pd.merge(occ_count_tagname, occ_count, on="tag_name")
    
    #merger new_occ_count avec booktags afin d'avoir new_tag_id, new_count
    new_book_tags = pd.merge(booktags, occ_count, on='tag_id' ) 

    new_tags = new_book_tags[['new_tag_id', 'tag_name']].drop_duplicates().sort_values('new_tag_id')
   
    new_tags = new_tags.reset_index(drop=True)
    #new_tags.drop(columns='index', inplace=True)

    #re-grouper les tags par new_tag_id et re-actulisé la valeur de count
    new_book_tags1 = pd.DataFrame(new_book_tags.drop(columns=['tag_id','count_y', 'tag_name'],axis=1).groupby(['goodreads_book_id', 'new_tag_id'])['count_x'].sum(), columns=['count_x']).reset_index()
    
    return  new_tags, new_book_tags1


def format_to_read(to_read: pd.DataFrame):
    """
        nettoyer et formatter des données de df to_read pour insérer dans BD
    """
    to_read.drop_duplicates(inplace=True)
    to_read.dropna(inplace=True)
    to_read = to_read.reset_index(drop=True)
    
    return to_read



########################## WIL

#    tags. to_sql('tags', if_exists='append', con=engine, index=False) #insertion dans tags
#    book_tags.to_sql('book_tags',if_exists='append', con=engine,index=False)
    