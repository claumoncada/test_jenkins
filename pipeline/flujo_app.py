# pipeline_lanzar_app.py
import subprocess
from prefect import task, flow
import os
import pickle
import pandas as pd

# Ruta de la app
APP_PATH = 'app.py'

# Tareas para cargar los modelos entrenados
@task
def cargar_modelos():
    with open('resultados_entrenamiento/knn_model.pkl', 'rb') as f:
        knn_model = pickle.load(f)

    with open('resultados_entrenamiento/reg_model.pkl', 'rb') as f:
        reg_model = pickle.load(f)
    
    return knn_model, reg_model

# Tarea para cargar los datos de las películas
@task
def cargar_datos_peliculas():
    movies = pd.read_csv('datasets/movies.csv')
    return movies

# Tarea para ejecutar la app Flask
@task
def lanzar_app():
    try:
        # Ejecutar la app de Flask utilizando subprocess
        subprocess.run(['python', APP_PATH], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar la app: {e}")
        raise e

# Definir el flujo principal
@flow(name="Pipeline de Lanzamiento de la App")
def pipeline_lanzar_app():
    # Cargar los modelos y datos de películas
    knn_model, reg_model = cargar_modelos()
    movies = cargar_datos_peliculas()

    # Iniciar la app de Flask
    lanzar_app()

    print("La aplicación Flask se ha lanzado correctamente.")

if __name__ == "__main__":
    pipeline_lanzar_app()
