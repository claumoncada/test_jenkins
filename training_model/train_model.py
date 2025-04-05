# train_models.py
import time
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

def train_knn(X_train, y_train):
    start_time = time.time()
    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(X_train, y_train)
    training_time = time.time() - start_time
    return knn, training_time

def train_linear_regression(X_train, y_train):
    start_time = time.time()
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    training_time = time.time() - start_time
    return reg, training_time

def save_model(model, filename):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)

def save_metrics(metrics, filename):
    with open(filename, 'wb') as f:
        pickle.dump(metrics, f)
