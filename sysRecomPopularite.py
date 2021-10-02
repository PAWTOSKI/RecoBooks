import pandas as pd
import numpy as np

class PoPRecommend():
    def __init__(self, dfRatings, dfBooks):
        self.dfRatings = dfRatings
        self.dfBooks = dfBooks
        self.rating_by_book = None


    def calculRatingByBook(self):
        """
            Calculer l'aggreation de nombre de fois de rating et le moyen de rating
            
            *** Params:
            dfRatings (DataFrame): de rating, qui contient des cols book_id, user_id, rating

            *** Return:
            Dataframe de book_id avec son rating moyen et son nombre de fois de vote.

        """
        ratings_by_livre = pd.DataFrame(self.dfRatings
                                        .groupby('book_id')['rating']
                                        .agg(func=['count', 'mean']))
        ratings_by_livre.reset_index(inplace=True)
        ratings_by_livre = ratings_by_livre.rename(columns={'mean':'avg_rating', 'count':'cnt_vote'}).reset_index()
    
        self.rating_by_book = ratings_by_livre
    

    def note_ponderee(self, x, mseuil, cmoyen):
        """
            caculer 
        """
        v = x['cnt_vote']
        r = x['avg_rating']
        return ((v*r/(v+mseuil))+(mseuil*cmoyen/(mseuil+v)))


    def populariteNotePonderer(self, nbLivres=30):
        """
            Trouver les 30 livres ayant dee scores pondérés les plus élevés.
            Les scores pondérés sont basés sur nombre de rating et le rating moyen du global 

            *** Params:
            
            *** Return:
            Dataframe de book_id avec son rating moyen et son nombre de fois de vote.
        """
        #ratingByBook = self.calculRatingByBook()
        # Quel est nombre de fois à noter qui se sépare les 25% des livres les mieux ratings
        # des 75% le moins bien noté ?
        
        nb_seuil = self.ratingByBook['cnt_vote'].quantile(0.75)
        #Calculer le rating moyen
        
        c_moyen = self.ratingByBook['avg_rating'].mean()
        
        #creer un df contenant des livres ayant au moins nb_seuil fois de voté
        q_ratings_livre = self.ratingByBook[self.ratingByBook['cnt_vote']>=nb_seuil].copy()
        q_ratings_livre.sort_values('book_id')

        #ajouter un col 'score' avec le note pondere selon nb_seuil, c_moyen
        q_ratings_livre['score'] = q_ratings_livre.apply(lambda x: self.note_ponderee(x, nb_seuil, c_moyen), axis=1)
        q_ratings_livre = q_ratings_livre.sort_values('score', ascending=False)
       
        #creer un dataframe result avec col bbok_id et score du 30 livres ayant des meilleurs scores
        #result = q_ratings_livre.iloc[:nbLivres][['book_id', 'score']]
        #result = pd.merge(result, self.dfBooks, on='book_id')
        #print(result)
        
        return q_ratings_livre


"""
print("Demarrer system ...")
print("1. Charger des donnees")
ratings = pd.read_csv('../donnees/ratings.csv')
books = pd.read_csv('../donnees/books.csv')
cols_book_affiche = ['book_id', 'original_title', 'title']
books = books[cols_book_affiche]
popRecom = PoPRecommend(ratings, books)
#ratings_livres = calculRatingByBook(ratings)
print("2. Saisir 1 chiffre - nombre de livre recommender: ")

nbLivres = int(input())
print("3. Creer liste de ", nbLivres, ' livres...\n')
list_livres_recomme = popRecom.populariteNotePonderer(nbLivres)
print('--- RESULTAT ---')
print(list_livres_recomme)
"""