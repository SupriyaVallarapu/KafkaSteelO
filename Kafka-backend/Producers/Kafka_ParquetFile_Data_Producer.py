# import os
# import time
# import pandas as pd
# from confluent_kafka import Producer
# import json
# from flask import Flask, request,Blueprint
# from flask_cors import CORS


# # app = Flask(__name__)
# # cors=CORS(app)

# parquet_blueprint = Blueprint('parquet_blueprint', __name__)

# producer = None
# processed_files = set()
# kafka_broker = None
# kafka_topic = None

# @parquet_blueprint.route('/api/parquetupload', methods=['POST'])
# def upload_parquet():
#     global producer, processed_files, kafka_broker, kafka_topic

# #  inputs
#     data_dir = request.json['data_dir']
#     new_kafka_broker = request.json['kafka_broker']
#     new_kafka_topic = request.json['kafka_topic']
#     new_time_column_name = request.json['time_column_name']


# # Create a producer if it doesn't exist or if the Kafka broker or topic has changed
#     if producer is None or new_kafka_broker != kafka_broker or new_kafka_topic != kafka_topic:
#         if producer is not None:
#             producer.flush()
#         kafka_broker = new_kafka_broker
#         kafka_topic = new_kafka_topic
#         producer = create_producer(kafka_broker, kafka_topic)
    
#     # List all parquet files in the directory
#     files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]

#     # Process any new files
#     for file in files:
#         if file not in processed_files:
#             process_file(os.path.join(data_dir, file), producer, new_time_column_name)

#     return 'Parquet Data uploaded to Kafka successfully!'

# # Create a producer to send data to Kafka
# def create_producer(kafka_broker, kafka_topic):
#     return Producer({
#     'bootstrap.servers': kafka_broker,
#     'queue.buffering.max.messages': 10000000,  # Set the desired queue size
#     'queue.buffering.max.ms': 500,
#     'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
#     'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
# })

# def process_file(filepath, producer, time_column_name):
#     # Load the parquet file into a pandas DataFrame
#     df = pd.read_parquet(filepath)

#     # Convert the 'Time' column to datetime if it's not already
#     df[time_column_name] = pd.to_datetime(df[time_column_name])

#     try:
#         for _, row in df.iterrows():
#             for column in df.columns:
#                 if column != time_column_name:
#                     timestamp = row[time_column_name].isoformat()
#                     value = row[column]
                    
#                     # Check if value is boolean and convert it
#                     if isinstance(value, bool):
#                         value = 1 if value else 0

#                     # Create a message to be sent to Kafka
#                     message = {
#                         'timestamp': timestamp,
#                         'sensor_name': column,
#                         'value': value
#                     }

#                     # Serialize the message to JSON
#                     message_json = json.dumps(message)

#                     # Send the message to Kafka
#                     producer.produce(topic=kafka_topic, value=message_json, key=column)
#             time.sleep(0.1)
#     finally:
#         # Close the producer
#         producer.flush()



# # import os
# # import time
# # import pandas as pd
# # from confluent_kafka import Producer
# # import json

# # # Get user inputs
# # data_dir = input("Enter the directory path containing the parquet files: ")
# # kafka_broker = input("Enter the Kafka broker (format - localhost:9092): ")
# # kafka_topic = input("Enter the Kafka topic: ")
# # time_column_name = input("Enter the name of the time column in your data: ")


# # # Create a producer to send data to Kafka
# # producer = Producer({
# #     'bootstrap.servers': kafka_broker,
# #     'queue.buffering.max.messages': 10000000,  # Set the desired queue size
# #     'queue.buffering.max.ms': 500,
# #     'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
# #     'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
# # })

# # def process_file(filepath, time_column_name):
# #     # Load the parquet file into a pandas DataFrame
# #     df = pd.read_parquet(filepath)

# #     # Convert the 'Time' column to datetime if it's not already
# #     df[time_column_name] = pd.to_datetime(df[time_column_name])

# #     try:
# #         for _, row in df.iterrows():
# #             for column in df.columns:
# #                 if column != time_column_name:
# #                     timestamp = row[time_column_name].isoformat()
# #                     value = row[column]
                    
# #                     # Check if value is boolean and convert it
# #                     if isinstance(value, bool):
# #                         value = 1 if value else 0

# #                     # Create a message to be sent to Kafka
# #                     message = {
# #                         'timestamp': timestamp,
# #                         'sensor_name': column,
# #                         'value': value
# #                     }

# #                     # Serialize the message to JSON
# #                     message_json = json.dumps(message)

# #                     # Send the message to Kafka
# #                     producer.produce(topic=kafka_topic, value=message_json, key=column)
# #             time.sleep(0.1)
# #     finally:
# #         # Close the producer
# #         producer.flush()

# # # Get the list of files already processed
# # processed_files = set()

# # while True:
# #     # List all parquet files in the directory
# #     files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]

# #     # Process any new files
# #     for file in files:
# #         if file not in processed_files:
# #             process_file(os.path.join(data_dir, file), time_column_name)
# #             processed_files.add(file)

# #     # Wait for a while before checking the directory again
# #     time.sleep(10)



from flask import Blueprint, request, jsonify
from flask_cors import CORS
import os
import time
import pandas as pd
from confluent_kafka import Producer, KafkaException
import json


parquet_blueprint = Blueprint('parquet_blueprint', __name__)


@parquet_blueprint.route('/api/parquetupload', methods=['POST'])
def upload_parquet():
    # Get the directory path, Kafka broker, and Kafka topic from the request
    data = request.get_json()

    # Ensure required fields are provided
    required_fields = ['data_dir', 'kafka_broker', 'kafka_topic', 'time_column_name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields in request data'}), 400

    data_dir = data['data_dir']
    kafka_broker = data['kafka_broker']
    kafka_topic = data['kafka_topic']
    time_column_name = data['time_column_name']

    # Check if data_dir exists
    if not os.path.isdir(data_dir):
        return jsonify({'error': f'Directory {data_dir} does not exist'}), 400

    # Check if there are any Parquet files in the directory
    files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]
    if not files:
        return jsonify({'error': f'No Parquet files found in directory {data_dir}'}), 400

    # Create a Kafka producer
    try:
        producer = create_producer(kafka_broker)
    except KafkaException as e:
        return jsonify({'error': f'Unable to connect to Kafka broker at {kafka_broker}. Error: {str(e)}'}), 500

    # Process any new files
    for file in files:
        try:
            process_file(os.path.join(data_dir, file), producer, kafka_topic, time_column_name)
        except Exception as e:
            return jsonify({'error': f'Error processing file {file}. Error: {str(e)}'}), 500

    return jsonify({'message': 'Parquet Data uploaded to Kafka successfully!'}), 200


def create_producer(kafka_broker):
    return Producer({
        'bootstrap.servers': kafka_broker,
        'queue.buffering.max.messages': 10000000,
        'compression.type': 'zstd'
    })


def process_file(filepath, producer, kafka_topic, time_column_name):
    # Load the Parquet file into a pandas DataFrame
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
        # Flush any outstanding messages
        producer.flush()
