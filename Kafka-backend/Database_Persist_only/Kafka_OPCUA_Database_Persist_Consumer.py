import time
from confluent_kafka import Consumer, KafkaError
import psycopg2
import json
import getpass

kafka_broker,offset,persist_data,consumer_group = "localhost:9092", "eng","no","testgroup"
# Get user inputs
kafka_broker = input("Enter the Kafka broker (default - localhost:9092): ") or kafka_broker
kafka_topic = input("Enter the Kafka topic: ")
offset = input("Enter where you want to read data from 'beginning' or 'end' (default - end): ") or offset
persist_data = input("Do you want to persist the data to TimescaleDB? (yes/no) (default - no): ") or persist_data
consumer_group = input("Enter the consumer group name you want your consumer to belong (default - testgroup): ") or consumer_group

db_name,db_schema,db_user,db_password,db_host,db_port = "kafka","kafkadata","postgres","postgres","localhost","5432"
# Database variables
if persist_data.lower() == 'yes':
    db_name = input("Enter your database name (default is kafka): ") or db_name
    db_schema = input("Enter your database name (default is kafkadata): ") or db_schema
    db_user = input("Enter your database username (default is postgres): ") or db_user
    db_password = getpass.getpass("Enter your database password (default is postgres): ") or db_password
    db_host = input("Enter your database host (default is localhost): ") or db_host
    db_port = input("Enter your database port (default is 5432): ") or db_port

# Create a consumer to consume data from Kafka
consumer = Consumer({
    'bootstrap.servers': kafka_broker,
    'group.id': consumer_group,
    'auto.offset.reset': offset
})

consumer.subscribe([kafka_topic])

def persist_to_timescaleDB(message_json, cur, conn):
    # Persist the data to TimescaleDB
    cur.execute(
        f"INSERT INTO {db_schema}.{kafka_topic} (sensor_name, value,timestamp) VALUES (%s, %s, %s)",
        (message_json['sensor_name'], message_json['value'],message_json['timestamp'])
    )
    conn.commit()

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
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {db_schema}.{kafka_topic} (
                    sensor_name VARCHAR(255),
                    value TEXT,
                    timestamp TIMESTAMPTZ NOT NULL
                );
            """)
            conn.commit()

        # Consume data from the Kafka topic
        message = consumer.poll(1.0)

        # if a message is received
        if message is not None:
            # if the message does not contain error
            if message.error() is None:
                message_json = json.loads(message.value().decode('utf-8'))

                # Persist the data to TimescaleDB
                persist_to_timescaleDB(message_json, cur, conn)
            elif message.error().code() != KafkaError._PARTITION_EOF:
                print(f"Error occurred: {message.error()}")
                if conn:
                    conn.close()
                time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {e}")
        if conn:
            conn.close()
        time.sleep(10)