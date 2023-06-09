import time
from confluent_kafka import Producer
import requests
import json
import psycopg2
from psycopg2 import sql
import getpass

# Get user inputs
api_url = input("Enter the URL of the API: ")
call_api_sec = int(input("How often do you want to call the API in seconds: "))
kafka_broker = input("Enter the Kafka broker (format - localhost:9092): ")
kafka_topic = input("Enter the Kafka topic: ")
persist_data = input("Do you want to persist the data to TimescaleDB? (yes/no): ")

# Database variables
if persist_data.lower() == 'yes':
    db_name = input("Enter your database name: ")
    db_user = input("Enter your database username: ")
    db_password = getpass.getpass("Enter your database password: ")
    db_host = input("Enter your database host (default is localhost): ")
    db_port = input("Enter your database port (default is 5432): ")

# Create a producer to send data to Kafka
producer = Producer({
    'bootstrap.servers': kafka_broker,
    'queue.buffering.max.messages': 10000000,  # Set the desired queue size
    'queue.buffering.max.ms': 500,
    'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
    'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
})

def get_api_data(api_url):
    response = requests.get(api_url)

    # Raise an error if the request was unsuccessful
    response.raise_for_status()

    return response.json()

def publish_to_kafka(data, cur=None, conn=None):
    # Serialize the message to JSON
    message_json = json.dumps(data)

    # Send the message to Kafka
    producer.produce(topic=kafka_topic, value=message_json)

    # Persist the data to TimescaleDB
    if conn:
        cur.execute(
            f"INSERT INTO kafkadata.{kafka_topic} (data) VALUES (%s)",
            (message_json,)
        )
        conn.commit()

    # Flush the producer
    producer.flush()

while True:
    conn = None
    cur = None
    try:
        # Create a connection to the database if user chose to persist data
        if persist_data.lower() == 'yes':
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )

            cur = conn.cursor()
            cur.execute(sql.SQL(f"""
                CREATE TABLE IF NOT EXISTS kafkadata.{kafka_topic} (
                    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    data JSONB
                );
            """).format(sql.Identifier(kafka_topic)))
            conn.commit()

        # Get the data from the API
        data = get_api_data(api_url)

        # Publish the data to Kafka
        publish_to_kafka(data, cur, conn)

        # Wait for a while before polling the API again
        time.sleep(10)

    except Exception as e:
        print(f"Error occurred: {e}")
        if conn:
            conn.close()
        time.sleep(call_api_sec)
