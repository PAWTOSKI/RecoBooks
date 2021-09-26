import pandas as pd


def format_books(data_books: pd.DataFrame):
    """
        nettoyer et formatter des données fournant par dataframe: books
        afin d'avoir un df books tout prête à insérer dans BD
        *** Params:
            data_books: dataframe étant chargé de fichier de données brutes
        *** Return:
            dataframe est prête d'inserer
    """
    ### Nettoyer



    ### preparer dataframe
    data_books = data_books.rename(
        columns = {
            "book_id": "book_id",
            "authors": "authors",
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
    
    return data_books


def format_tags(data_tags: pd.DataFrame):
    """
        préparer df tags afin d'avoir un df prête à insérer dans BD
    """
    
    ###
    # ajouter partie nettoyer ou appelle fonction de traiter des tags
    
    data_tags = data_tags.rename(
        columns = {
            "id_tag": "id_id_tag",
            "tag_name": "tag_name"
                }
        )
    data_tags.index += 1
    
    return data_tags


def format_ratings(data_ratings: pd.DataFrame):
    """
        afin d'avoir un df ratings tout prête à insérer dans BD
    """

    data_ratings = data_ratings.rename(
            columns = {
                "id": "user_id",
                "book_id": "book_id"
                    }
        )
    ### ??? 
    data_ratings.index += 1
    
    return data_ratings


def format_to_read(to_read: pd.DataFrame):
    """
        nettoyer et formatter des données fournant par dataframe: books
        afin d'avoir un df books tout prête à insérer dans BD
    """
    
    
    return to_read


def format_book_tags(data_book_tags: pd.DataFrame):
    """
        nettoyer et formatter des données fournant par dataframe: books
        afin d'avoir un df books tout prête à insérer dans BD
    """

    data_book_tags = data_book_tags.rename(
            columns = {
                "goodreads_book_id": "goodreads_book_id",
                "tag_id": "tag_id"
                    }
        )
    data_book_tags.index += 1
    
    return data_book_tags


def format_user(data_users: pd.DataFrame):
    """
        
    """
    data_users = data_users.rename(
        columns={
            "id": "id",
            "name": "name", 
            "password":"password"
                }
        )
    data_users.index += 1        
    
    return data_users