from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Cargar datos de películas
movies = pd.read_csv('datasets/movies.csv')  # Asegúrate de que el archivo esté en la ruta correcta

# Cargar los modelos entrenados
with open('knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)

with open('reg_model.pkl', 'rb') as f:
    reg_model = pickle.load(f)

# Cargar la matriz de usuarios y películas
ratings = pd.read_csv('datasets/ratings.csv')
user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

# Función para obtener recomendaciones
def recommend_movies(model, user_id):
    peliculas_no_calificadas = user_item_matrix.loc[user_id] == 0
    peliculas_no_calificadas = peliculas_no_calificadas[peliculas_no_calificadas].index

    # Predecir calificaciones para esas películas con el modelo
    X = np.array([[user_id, movie_id] for movie_id in peliculas_no_calificadas])
    predicciones = model.predict(X)

    # Crear un DataFrame con las predicciones
    recomendaciones = pd.DataFrame({
        'movieId': peliculas_no_calificadas,
        'predicciones': predicciones
    })

    # Ordenar las películas por la calificación predicha más alta
    recomendaciones = recomendaciones.sort_values(by='predicciones', ascending=False)

    # Obtener los títulos de las películas recomendadas
    top_recomendaciones = recomendaciones.head(5)
    movie_titles = [movies[movies['movieId'] == movie_id]['title'].values[0] for movie_id in top_recomendaciones['movieId']]

    return movie_titles

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Obtener el ID de usuario del formulario
    try:
        user_id = int(request.form['user_id'])
    except ValueError:
        return render_template('result.html', recommendations=["ID de usuario inválido."])

    # Verificar si el user_id existe en el conjunto de datos
    if user_id not in user_item_matrix.index:
        return render_template('result.html', recommendations=["ID de usuario no encontrado."])

    model_type = request.form['model']

    # Selección del modelo basado en el botón elegido
    if model_type == 'knn':
        recommendations = recommend_movies(knn_model, user_id)
    elif model_type == 'reg':
        recommendations = recommend_movies(reg_model, user_id)
    else:
        recommendations = ["Modelo no válido"]

    return render_template('result.html', recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)

