import os
import time
import pandas as pd
from confluent_kafka import Producer
import json
import psycopg2
from psycopg2 import sql
import getpass

# Get user inputs
data_dir = input("Enter the directory path containing the parquet files: ")
kafka_broker = input("Enter the Kafka broker (format - localhost:9092): ")
kafka_topic = input("Enter the Kafka topic: ")
time_column_name = input("Enter the name of the time column in your data: ")
persist_data = input("Do you want to persist the data to TimescaleDB? (yes/no): ")

# Database variables (fill this with your own info)
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

def process_file(filepath, time_column_name, cur=None, conn=None):
    # Load the parquet file into a pandas DataFrame
    df = pd.read_parquet(filepath)

    # Convert the 'Time' column to datetime if it's not already
    df[time_column_name] = pd.to_datetime(df[time_column_name])

    # Counter for batch commit
    counter = 0
    try:
        for _, row in df.iterrows():
            for column in df.columns:
                if column != time_column_name:
                    timestamp = row[time_column_name].isoformat()
                    value = row[column]
                    
                    # Check if value is boolean and convert it
                    if isinstance(value, bool):
                        value = 1 if value else 0

                    # Create a message to be sent to Kafka
                    message = {
                        'timestamp': timestamp,
                        'sensor_name': column,
                        'value': value
                    }

                    # Serialize the message to JSON
                    message_json = json.dumps(message)

                    # Send the message to Kafka
                    producer.produce(topic=kafka_topic, value=message_json, key=column)

                    # Persist the data to TimescaleDB
                    if conn and cur:
                        cur.execute(
                            f"INSERT INTO kafkadata.{kafka_topic} (timestamp, data) VALUES (%s, %s)",
                            (timestamp, message_json)
                        )

                        counter += 1
                        if counter >= 100:  # Commit every 100 inserts
                            conn.commit()
                            counter = 0

            time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Flush any outstanding messages
        producer.flush()

        # Commit any remaining inserts
        if conn:
            conn.commit()

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

            # Create a cursor object
            cur = conn.cursor()

            # Create a table if it doesn't exist
            cur.execute(sql.SQL(f"""
                CREATE TABLE IF NOT EXISTS kafkadata.{kafka_topic} (
                    timestamp TIMESTAMPTZ NOT NULL,
                    data JSONB
                );
            """).format(sql.Identifier(kafka_topic)))

            conn.commit()

        # List all parquet files in the directory
        files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]

        # Process any new files
        for file in files:
            if file not in processed_files:
                process_file(os.path.join(data_dir, file), time_column_name, cur, conn)
                processed_files.add(file)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the database connection
        if conn:
            cur.close()
            conn.close()

    # Wait for a while before checking the directory again
    time.sleep(10)
