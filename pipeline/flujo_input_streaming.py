# streaming_pipeline.py
from prefect import task, flow
from get_streaming_ratings import KafkaCSVConsumer  # Importamos la clase de tu script

# Definir una tarea de Prefect que ejecute el consumidor Kafka
@task
def ejecutar_get_streaming_ratings():
    consumer = KafkaCSVConsumer()
    consumer.consume_messages()  # Empieza a consumir mensajes desde Kafka
    return "Consumo de mensajes completo"

# Crear el flujo
@flow(name="Pipeline Get Streaming Ratings")
def pipeline_get_streaming_ratings():
    resultado = ejecutar_get_streaming_ratings()
    print(f"Resultado del pipeline de get streaming ratings: {resultado}")

if __name__ == "__main__":
    pipeline_get_streaming_ratings()
