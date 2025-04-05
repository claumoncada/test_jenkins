pipeline {
    agent any
    
    environment {
        PROJECT_DIR = '/ruta/a/tu/proyecto'
        RESULTS_DIR = '/ruta/a/resultados_entrenamientos'
    }
    
    stages {
        stage('Preparar Entorno') {
            steps {
                script {
                    // Levanta servicios de Docker como Kafka
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
        
        stage('Clonar Repositorio') {
            steps {
                script {
                    // Clonar el repositorio en el contenedor
                    sh 'git clone https://github.com/usuario/proyecto.git $PROJECT_DIR'
                }
            }
        }
        
        stage('Entrenamiento del Modelo') {
            steps {
                script {
                    // Ejecuta el script de entrenamiento
                    sh 'python3 $PROJECT_DIR/entrenamiento.py'
                }
            }
        }

        stage('Ejecutar Flujos de Prefect') {
            steps {
                script {
                    // Ejecuta los flujos de Prefect para el procesamiento y streaming de datos
                    sh 'python3 $PROJECT_DIR/flujo_get_streamming.py'
                    sh 'python3 $PROJECT_DIR/flujo_input_streamming.py'
                }
            }
        }
        
        stage('Evaluación del Modelo') {
            steps {
                script {
                    // Ejecuta el script para la evaluación del modelo
                    sh 'python3 $PROJECT_DIR/flujo_entrenamiento_modelo.py'
                }
            }
        }
        
        stage('Despliegue de la Aplicación') {
            steps {
                script {
                    // Despliega la aplicación
                    sh 'python3 $PROJECT_DIR/app.py'
                }
            }
        }

        stage('Generar Resultados y Métricas') {
            steps {
                script {
                    // Guarda los resultados y las métricas en el directorio de resultados
                    sh 'cp -r $PROJECT_DIR/resultados_entrenamientos/* $RESULTS_DIR/'
                }
            }
        }

        stage('Parar Entorno') {
            steps {
                script {
                    // Detiene los servicios de Docker (Kafka, etc.)
                    sh 'docker-compose -f docker-compose.yml down'
                }
            }
        }
    }

    post {
        always {
            // Esto se ejecutará siempre, independientemente del estado del pipeline
            echo 'Pipeline completado.'
        }
        success {
            echo 'El pipeline ha finalizado con éxito.'
        }
        failure {
            echo 'El pipeline ha fallado.'
        }
    }
}
