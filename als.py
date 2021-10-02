import pandas as pd
import sqlalchemy as sql
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import seaborn as sns
import numpy as np
from sklearn.metrics import mean_squared_error

def matrixRating (ratings):
    """
    Creation de la matrise d'interactions
    """
    nbr_user=ratings['user_id'].unique().shape[0]
    nbr_book=ratings['book_id'].unique().shape[0]
    ratings_matrix=np.zeros((nbr_user,nbr_book))
    for row in ratings.itertuples(index = False):
        ratings_matrix[row.user_id - 1, row.book_id - 1] = row.rating
    return ratings_matrix 

def create_train_test(ratings):
    """
    split into training and test sets,
    remove 10 ratings from each user
    and assign them to the test set
    """
    test = np.zeros(ratings.shape)
    train = ratings.copy()
    for user in range(ratings.shape[0]):
        test_index = np.random.choice(
            np.flatnonzero(ratings[user]), size = 10, replace = False)

        train[user, test_index] = 0.0
        test[user, test_index] = ratings[user, test_index]
        
    # assert that training and testing set are truly disjoint
    assert np.all(train * test == 0)
    return train, test

class ExplicitMF:
    """
    Entraîner un modèle de factorisation matricielle à l’aide des moindres carrés alternatifs
    pour prédire les entrées vides dans une matrice
    
    Parameters
    ----------
    n_iters : int
        nombre d’itérations pour entraîner l’algorithme
        
    n_factors : int
        nombre de facteurs latents à utiliser dans le modèle 
        de factorisation matricielle, certaines bibliothèques 
        d’apprentissage automatique désignent cela comme rang
        
        
    reg : float
        terme de régularisation pour les facteurs latents 
        élément/utilisateur, puisque lambda est un mot-clé 
        en python, nous utilisons reg à la place
        
    """

    def __init__(self, n_iters, n_factors, reg):
        self.reg = reg
        self.n_iters = n_iters
        self.n_factors = n_factors  
        
    def fit(self, train, test):
        """
        réussir la formation et les tests en même temps 
        pour enregistrer la convergence du modèle, 
        en supposant que les deux ensembles de données 
        se trouvent sous la forme d’une matrice Utilisateur 
        x Élément avec des cellules comme évaluations
        
        """
        self.n_user, self.n_book = train.shape
        self.user_factors = np.random.random((self.n_user, self.n_factors))
        self.book_factors = np.random.random((self.n_book, self.n_factors))
        
        # record the training and testing mse for every iteration
        # to show convergence later (usually, not worth it for production)
        self.test_mse_record  = []
        self.train_mse_record = []   
        for _ in range(self.n_iters):
            self.user_factors = self._als_step(train, self.user_factors, self.book_factors)
            self.book_factors = self._als_step(train.T, self.book_factors, self.user_factors) 
            predictions = self.predict()
            test_mse = self.compute_mse(test, predictions)
            train_mse = self.compute_mse(train, predictions)
            self.test_mse_record.append(test_mse)
            self.train_mse_record.append(train_mse)
        
        return self    
    
    def _als_step(self, ratings, solve_vecs, fixed_vecs):
        """
        lors de la mise à jour de la matrice utilisateur, 
        la matrice d’éléments est le vecteur fixe et vice versa
        
        """
        A = fixed_vecs.T.dot(fixed_vecs) + np.eye(self.n_factors) * self.reg
        b = ratings.dot(fixed_vecs)
        A_inv = np.linalg.inv(A)
        solve_vecs = b.dot(A_inv)
        return solve_vecs
    
    def predict(self):
        """predict ratings for every user and item"""
        pred = self.user_factors.dot(self.book_factors.T)
        return pred
    
    @staticmethod
    def compute_mse(y_true, y_pred):
        """ignore zero terms prior to comparing the mse"""
        mask = np.nonzero(y_true)
        mse = mean_squared_error(y_true[mask], y_pred[mask])
        return mse
    
    def bookRecom(user_id,model,books):
        prdt=model.predict()
        l=sorted(list(prdt[user_id]),reverse=True)
        return books[books['book_id']].isin([l.index(e) for e in l if 4<=e<=5][:10])
