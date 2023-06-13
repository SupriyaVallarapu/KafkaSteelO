import os
import time
import pandas as pd
from confluent_kafka import Producer
import json
import psycopg2
from psycopg2 import sql
import getpass

# Get user inputs
data_dir = input("Enter the directory path containing the CSV files: ")
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
    'queue.buffering.max.ms': 0,
    'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
    'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
})


def process_file(filepath, cur=None, conn=None):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(filepath)

    try:
        for _, row in df.iterrows():
            # Convert each row to a dictionary
            row_dict = row.to_dict()

            # Serialize the row to JSON
            message_json = json.dumps(row_dict)

            # Send the message to Kafka
            producer.produce(topic=kafka_topic, value=message_json)

            # Persist the data to TimescaleDB
            if conn:
                cur.execute(
                    f"INSERT INTO kafkadata.{kafka_topic} (data) VALUES (%s)",
                    (message_json,)
                )
                conn.commit()
            
            time.sleep(0.1)
    finally:
        # Flush any outstanding messages
        producer.flush()
        
        # Close the database connection
        if conn:
            cur.close()
            conn.close()

# Get the list of files already processed
processed_files = set()

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

        # List all CSV files in the directory
        files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

        # Process any new files
        for file in files:
            if file not in processed_files:
                process_file(os.path.join(data_dir, file), cur, conn)
                processed_files.add(file)

        # Wait for a while before checking the directory again
        time.sleep(10)

    except Exception as e:
        print(f"Error occurred: {e}")
        if conn:
            conn.close()
        time.sleep(10)
