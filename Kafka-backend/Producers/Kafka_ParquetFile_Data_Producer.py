
import threading
import pandas as pd
import time
import os
from confluent_kafka import Producer, KafkaException
from flask import Blueprint, request, jsonify
import json

parquet_blueprint = Blueprint('parquet_blueprint', __name__)

@parquet_blueprint.route('/api/parquetupload', methods=['POST'])
def start_process():
    data = request.get_json()

    required_fields = ['data_dir', 'kafka_broker', 'kafka_topic', 'time_column_name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields in request data'}), 400

    data_dir = data['data_dir']
    kafka_broker = data['kafka_broker']
    kafka_topic = data['kafka_topic']
    time_column_name = data['time_column_name']

    if not os.path.isdir(data_dir):
        return jsonify({'error': f'Directory {data_dir} does not exist'}), 400

    try:
        producer = create_producer(kafka_broker)
    except KafkaException as e:
        return jsonify({'error': f'Unable to connect to Kafka broker at {kafka_broker}. Error: {str(e)}'}), 500

    threading.Thread(target=collect_and_stream_data, args=(data_dir, producer, kafka_topic, time_column_name)).start()

    return jsonify({'message': 'Parquet data upload process started.'}), 200

def collect_and_stream_data(data_dir, producer, kafka_topic, time_column_name):
    processed_files = set()

    while True:
        try:
            files = [f for f in os.listdir(data_dir) if f.endswith('.parquet') and f not in processed_files]

            for file in files:
                process_file(os.path.join(data_dir, file), producer, kafka_topic, time_column_name)
                processed_files.add(file)

        except Exception as e:
            print(f"Error occurred: {e}")

        time.sleep(10)  # wait for 10 seconds before next directory check

def create_producer(kafka_broker):
    return Producer({
        'bootstrap.servers': kafka_broker,
        'enable.idempotence': True,
        'queue.buffering.max.messages': 10000000,
        'compression.type': 'zstd',
        'queue.buffering.max.ms': 500,
        'acks': 'all'
    })

def process_file(filepath, producer, kafka_topic, time_column_name):
    df = pd.read_parquet(filepath)
    df[time_column_name] = pd.to_datetime(df[time_column_name])

    try:
        for _, row in df.iterrows():
            for column in df.columns:
                if column != time_column_name:
                    timestamp = row[time_column_name].isoformat()
                    value = row[column]
                    if isinstance(value, bool):
                        value = 1 if value else 0

                    message = {
                        'timestamp': timestamp,
                        'sensor_name': column,
                        'value': value
                    }
                    message_json = json.dumps(message)
                    producer.produce(topic=kafka_topic, value=message_json, key=column)
    finally:
        producer.flush()
