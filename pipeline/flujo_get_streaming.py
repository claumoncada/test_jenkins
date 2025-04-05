# streaming_pipeline.py
from prefect import task, flow
from input_streaming_ratings import KafkaCSVProducer  # Importamos la clase de tu script

# Definir una tarea de Prefect que ejecute el productor Kafka
@task
def ejecutar_input_streaming():
    producer = KafkaCSVProducer()
    if producer.connect():
        producer.simulate_transmission("datasets/ratings.csv")  # Asegúrate de tener el archivo CSV disponible
    return "Simulación de transmisión completa"

# Crear el flujo
@flow(name="Pipeline Input Streaming")
def pipeline_input_streaming():
    resultado = ejecutar_input_streaming()
    print(f"Resultado del pipeline de input streaming: {resultado}")

if __name__ == "__main__":
    pipeline_input_streaming()
