def clean_data_books(data_books: DataFrame):

#suppresion des doubons
    data_books.drop_duplicates(inplace=True)

#nettoyage et uniformisation des labels de titres originaux. En effet, il est a été adopter par convention par les
# auteurs qu'une valeur manquante dans ce champ d'un film signifie que ce film n'a été publié qu'en une seule édition.
# Par conséquent, le champ "Title" équivaut au champ "Original_title" dans ce cas de figure et il convient d'insérer dans
# une valeur par défaut dans le champ "Original_title". 


    mask=data_books["original_title"].isna()
    data_books.loc[mask,"original_title"]=='0'
    return data_books

#suppresion des doubons
    data_books.dropna(inplace=True)




def clean_data_ratings(data_ratings: DataFrame):

    #suppresion des doubons
    data_ratings.drop_duplicates(inplace=True)

    #suppresion des doubons
    data_ratings.dropna(inplace=True)    

    return data_ratings



def clean_data_users( data_users : DataFrame):

    #suppresion des doubons
    data_users.drop_duplicates(inplace=True)

    #suppresion des doubons
    data_users.dropna(inplace=True)    

    return data_users



def clean_data_tags( data_tags : DataFrame):

    #suppresion des doubons
    data_tags.drop_duplicates(inplace=True)

    #suppresion des doubons
    data_tags.dropna(inplace=True)    

    return data_tags



def clean_data_books_tags( ddata_books_tags : DataFrame):

    #suppresion des doubons
    data_books_tags.drop_duplicates(inplace=True)

    #suppresion des doubons
    data_books_tags.dropna(inplace=True)    

    return data_books_tags





