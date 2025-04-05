import os
import csv
import pickle
import time
from prefect import task, flow
from preprocessing import load_data, create_user_item_matrix, split_data
from train_models import train_knn, train_linear_regression, save_model, save_metrics
from predict import evaluate_model

# Directorio para guardar los resultados
RESULTADOS_DIR = 'resultados_entrenamiento'
if not os.path.exists(RESULTADOS_DIR):
    os.makedirs(RESULTADOS_DIR)

# Cargar datos
@task
def cargar_datos():
    ratings, movies = load_data('datasets/ratings.csv', 'datasets/movies.csv')
    return ratings, movies

# Preprocesamiento de datos
@task
def preprocesar_datos(ratings):
    X = create_user_item_matrix(ratings)
    X_train, y_train, X_test, y_test = split_data(ratings)
    return X_train, y_train, X_test, y_test

# Entrenamiento y evaluación del modelo KNN
@task
def entrenar_knn(X_train, y_train, X_test, y_test):
    knn, knn_training_time = train_knn(X_train, y_train)
    knn_predictions, knn_mse = evaluate_model(knn, X_test, y_test)
    return knn, knn_training_time, knn_mse

# Entrenamiento y evaluación del modelo de Regresión Lineal
@task
def entrenar_regresion_lineal(X_train, y_train, X_test, y_test):
    reg, reg_training_time = train_linear_regression(X_train, y_train)
    reg_predictions, reg_mse = evaluate_model(reg, X_test, y_test)
    return reg, reg_training_time, reg_mse

# Guardar modelos entrenados
@task
def guardar_modelos(knn, reg):
    save_model(knn, os.path.join(RESULTADOS_DIR, 'knn_model.pkl'))
    save_model(reg, os.path.join(RESULTADOS_DIR, 'reg_model.pkl'))

# Guardar métricas de entrenamiento en un archivo CSV
@task
def guardar_metricas_csv(knn_training_time, knn_mse, reg_training_time, reg_mse):
    metrics_file = os.path.join(RESULTADOS_DIR, 'metricas.csv')
    with open(metrics_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Si el archivo está vacío, agregar los encabezados
            writer.writerow(['Modelo', 'Tiempo de Entrenamiento (s)', 'MSE'])
        
        writer.writerow(['KNN', knn_training_time, knn_mse])
        writer.writerow(['Regresión Lineal', reg_training_time, reg_mse])

# Definir el flujo principal
@flow(name="Pipeline de Entrenamiento de Modelos")
def pipeline_entrenamiento():
    # Cargar datos
    ratings, movies = cargar_datos()
    
    # Preprocesar los datos
    X_train, y_train, X_test, y_test = preprocesar_datos(ratings)
    
    # Entrenar y evaluar modelos
    knn, knn_training_time, knn_mse = entrenar_knn(X_train, y_train, X_test, y_test)
    reg, reg_training_time, reg_mse = entrenar_regresion_lineal(X_train, y_train, X_test, y_test)
    
    # Guardar modelos entrenados
    guardar_modelos(knn, reg)
    
    # Guardar las métricas en archivo CSV
    guardar_metricas_csv(knn_training_time, knn_mse, reg_training_time, reg_mse)

    print("Modelos entrenados y resultados guardados en la carpeta 'resultados_entrenamiento'.")

if __name__ == "__main__":
    pipeline_entrenamiento()
