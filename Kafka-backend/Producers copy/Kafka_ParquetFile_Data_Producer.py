import os
import time
import pandas as pd
from confluent_kafka import Producer
import json

# Get user inputs
kafka_broker = "localhost:9092"
data_dir = input("Enter the directory path containing the parquet files: ")
kafka_broker = input("Enter the Kafka broker (format - localhost:9092): ") or kafka_broker
kafka_topic = input("Enter the Kafka topic: ")
time_column_name = input("Enter the name of the time column in your data: ")


# Create a producer to send data to Kafka
producer = Producer({
    'bootstrap.servers': kafka_broker,
    'enable.idempotence': True,
    'queue.buffering.max.messages': 10000000,  # Set the desired queue size
    'queue.buffering.max.ms': 500,
    'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
    'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
})

def process_file(filepath, time_column_name):
    # Load the parquet file into a pandas DataFrame
    df = pd.read_parquet(filepath)

    # Convert the 'Time' column to datetime if it's not already
    df[time_column_name] = pd.to_datetime(df[time_column_name])

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
            time.sleep(0.1)
    finally:
        # Close the producer
        producer.flush()

# Get the list of files already processed
processed_files = set()

while True:
    # List all parquet files in the directory
    files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]

    # Process any new files
    for file in files:
        if file not in processed_files:
            process_file(os.path.join(data_dir, file), time_column_name)
            processed_files.add(file)

    # Wait for a while before checking the directory again
    time.sleep(10)
