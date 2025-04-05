import socket
import logging
import csv
from kafka import KafkaConsumer
from datetime import datetime

# Configuración de Kafka
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'input_streaming_ratings'
CSV_FILE = 'ratings_nuevo.csv'  # Archivo CSV en lugar de base de datos

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear archivo CSV si no existe
def create_csv_file():
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Escribir encabezado si el archivo está vacío
            if file.tell() == 0:
                writer.writerow(['etl_timestamp', 'userId', 'movieId', 'rating', 'timestamp'])
    except Exception as e:
        logger.error(f"❌ Error creando el archivo CSV: {str(e)}")

class KafkaCSVConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset='earliest',
            value_deserializer=lambda x: x.decode('utf-8')
        )
   
    def consume_messages(self):
        create_csv_file()  # Asegurarse de que el archivo CSV exista y tenga encabezado
        
        for message in self.consumer:
            print(message.value)
            message_content = message.value
            insert_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if "Mensaje aleatorio generado" in message_content:
                self.log_to_csv(insert_timestamp, "BAD")
            else:
                try:
                    parts = message_content.split(", ")
                    etl_timestamp = parts[0]
                    userId, movieId, rating, timestamp = map(str.strip, parts[1:])
                   
                    # Escribir en el archivo CSV
                    self.write_to_csv(etl_timestamp, userId, movieId, rating, timestamp)
                    self.log_to_csv(insert_timestamp, "OK")
                except Exception as e:
                    self.log_to_csv(insert_timestamp, "BAD")
                    logger.error(f"❌ Error procesando mensaje: {str(e)}")
   
    def write_to_csv(self, etl_timestamp, userId, movieId, rating, timestamp):
        try:
            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([etl_timestamp, userId, movieId, rating, timestamp])
        except Exception as e:
            logger.error(f"❌ Error escribiendo en el CSV: {str(e)}")

    def log_to_csv(self, insert_timestamp, status):
        try:
            with open('logs.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([insert_timestamp, status])
        except Exception as e:
            logger.error(f"❌ Error escribiendo en el archivo de logs: {str(e)}")

if __name__ == "__main__":
    consumer = KafkaCSVConsumer()
    consumer.consume_messages()
