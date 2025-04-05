# main.py
import time
from preprocessing import load_data, create_user_item_matrix, split_data
from train_models import train_knn, train_linear_regression, save_model, save_metrics
from predict import evaluate_model

# Cargar datos
ratings, movies = load_data('ratings.csv', 'movies.csv')

# Preprocesar datos
X = create_user_item_matrix(ratings)
X_train, y_train, X_test, y_test = split_data(ratings)

# Diccionario para guardar métricas
metrics = {}

# Entrenamiento de KNN
knn, knn_training_time = train_knn(X_train, y_train)
print(f"Tiempo de entrenamiento para KNN: {knn_training_time} segundos")

# Evaluación de KNN
knn_predictions, knn_mse = evaluate_model(knn, X_test, y_test)
print(f"MSE para KNN: {knn_mse}")
metrics['knn_training_time'] = knn_training_time
metrics['knn_mse'] = knn_mse

# Entrenamiento de Regresión Lineal
reg, reg_training_time = train_linear_regression(X_train, y_train)
print(f"Tiempo de entrenamiento para Regresión Lineal: {reg_training_time} segundos")

# Evaluación de Regresión Lineal
reg_predictions, reg_mse = evaluate_model(reg, X_test, y_test)
print(f"MSE para Regresión Lineal: {reg_mse}")
metrics['reg_training_time'] = reg_training_time
metrics['reg_mse'] = reg_mse

# Guardar modelos
save_model(knn, 'knn_model.pkl')
save_model(reg, 'reg_model.pkl')

# Guardar métricas
save_metrics(metrics, 'models/metrics.pkl')

print("Modelos entrenados y guardados con métricas.")
