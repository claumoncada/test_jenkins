# preprocessing.py
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(ratings_file, movies_file):
    # Cargar los datos
    ratings = pd.read_csv(ratings_file)
    movies = pd.read_csv(movies_file)
    return ratings, movies

def create_user_item_matrix(ratings):
    # Crear la matriz usuario-item
    user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    X = user_item_matrix.values
    return X

def split_data(ratings):
    # Crear conjuntos de entrenamiento y prueba
    train_data, test_data = train_test_split(ratings, test_size=0.2, random_state=42)
    X_train = train_data[['userId', 'movieId']].values  # Dos características
    y_train = train_data['rating'].values
    X_test = test_data[['userId', 'movieId']].values
    y_test = test_data['rating'].values
    return X_train, y_train, X_test, y_test
