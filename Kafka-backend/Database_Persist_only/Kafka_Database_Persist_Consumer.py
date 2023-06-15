# import time
# from confluent_kafka import Consumer
# import json
# import psycopg2
# import getpass

# kafka_broker,offset,persist_data,consumer_group = "localhost:9092", "eng","no","testgroup"
# # Get user inputs
# data_source = input("Enter the data source (api/csv/parquet): ")
# kafka_broker = input("Enter the Kafka broker (default - localhost:9092): ") or kafka_broker
# kafka_topic = input("Enter the Kafka topic: ")
# offset = input("Enter where you want to read data from 'beginning' or 'end' (default - end): ") or offset
# persist_data = input("Do you want to persist the data to TimescaleDB? (yes/no) (default - no): ") or persist_data
# consumer_group = input("Enter the consumer group name you want your consumer to belong (default - testgroup): ") or consumer_group

# db_name,db_schema,db_user,db_password,db_host,db_port = "kafka","kafkadata","postgres","postgres","localhost","5432"
# # Database variables
# if persist_data.lower() == 'yes':
#     db_name = input("Enter your database name (default is kafka): ") or db_name
#     db_schema = input("Enter your database name (default is kafkadata): ") or db_schema
#     db_user = input("Enter your database username (default is postgres): ") or db_user
#     db_password = getpass.getpass("Enter your database password (default is postgres): ") or db_password
#     db_host = input("Enter your database host (default is localhost): ") or db_host
#     db_port = input("Enter your database port (default is 5432): ") or db_port

# # Create a consumer to consume data from Kafka
# consumer = Consumer({
#     'bootstrap.servers': kafka_broker,
#     'group.id': consumer_group,
#     'auto.offset.reset': offset
# })

# consumer.subscribe([kafka_topic])

# def persist_to_timescaleDB(message, cur, conn):
#     # Serialize the message to JSON
#     message_json = json.dumps(message)

#     # Persist the data to TimescaleDB
#     cur.execute(
#         f"INSERT INTO {db_schema}.{kafka_topic} (data) VALUES (%s)",
#         (message_json,)
#     )
#     conn.commit()

# while True:
#     conn = None
#     cur = None
#     try:
#         # Create a connection to the database if user chose to persist data
#         if persist_data.lower() == 'yes':
#             conn = psycopg2.connect(
#                 dbname=db_name,
#                 user=db_user,
#                 password=db_password,
#                 host=db_host,
#                 port=db_port
#             )

#             cur = conn.cursor()
#             cur.execute(f"""
#                 CREATE TABLE IF NOT EXISTS {db_schema}.{kafka_topic} (
#                     timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
#                     data JSONB
#                 );
#             """)
#             conn.commit()

#         # Consume data from the Kafka topic
#         message = consumer.poll(1.0)

#         # if a message is received
#         if message is not None:
#             # if the message does not contain error
#             if message.error() is None:
#                 message = json.loads(message.value().decode('utf-8'))

#                 # Persist the data to TimescaleDB
#                 persist_to_timescaleDB(message, cur, conn)
#             elif message.error().code() != KafkaError._PARTITION_EOF:
#                 print(f"Error occurred: {message.error()}")
#                 if conn:
#                     conn.close()
#                 time.sleep(1)

#     except Exception as e:
#         print(f"Error occurred: {e}")
#         if conn:
#             conn.close()
#         time.sleep(10)





from flask import Flask, request
from flask_cors import CORS,cross_origin
from confluent_kafka import Consumer, TopicPartition, KafkaError
import json
import psycopg2
from getpass import getpass
import traceback
app = Flask(__name__)
cors=CORS(app)

cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:8081", "http://localhost:3000"]}})

@app.route('/consume_and_persist', methods=['POST'])
@cross_origin()
def consume_and_persist():
    # Get the JSON body of the request
    request_body = request.json

    # Get the parameters from the JSON body
    kafka_broker = request_body.get('kafka_broker')
    kafka_topic = request_body.get('kafka_topic')
    offset = request_body.get('offset')

    db_name = request_body.get('db_name')
    db_schema = request_body.get('db_schema')
    db_user = request_body.get('db_user')
    db_password = request_body.get('db_password')
    db_host = request_body.get('db_host')
    db_port = request_body.get('db_port')

    # Create a Kafka consumer
    consumer = Consumer({
        'bootstrap.servers': kafka_broker,
        'group.id': 'testgroup',
        'auto.offset.reset': 'earliest'
    })

    if offset.lower() == 'beginning':
        consumer.assign([TopicPartition(kafka_topic, 0, 0)])  # Start from the beginning
    elif offset.lower() == 'end':
        consumer.assign([TopicPartition(kafka_topic, 0, consumer.get_watermark_offsets(TopicPartition(kafka_topic, 0))[1] - 1)])  # Start from the end
    else:
        consumer.assign([TopicPartition(kafka_topic, 0, int(offset))])  # Start from user-defined offset

    conn = None
    cur = None
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cur = conn.cursor()

        # Create a table for the Kafka topic if it doesn't exist
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_schema}.{kafka_topic} (
                timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                data JSONB
            );
        """)
        conn.commit()

        # Consume data from Kafka and persist each message to the database
        while True:
             msg = consumer.poll(1.0)
             if msg is None:
                continue
             if msg.error():
                return {"error": f"Consumer error: {msg.error()}"}, 500
             else:
                data_type = type(msg.value())
                print(f"Incoming data type: {data_type}")
                if data_type == bytes:
                    try:
                        cur.execute(
                            f"INSERT INTO {db_schema}.{kafka_topic} (data) VALUES (%s)",
                            (json.dumps(msg.value().decode('utf-8')),)
                        )
                        conn.commit()
                    except Exception as e:
                        traceback_str = traceback.format_exc()
                        print(f"Error occurred in SQL execution: {traceback_str}")
                else:
                    print("Data type not handled.")

    except Exception:
        traceback_str = traceback.format_exc()
        return {"error": f"Error occurred: {traceback_str}"}, 500
    finally:
        if conn:
            conn.close()
        consumer.close()

        return {"message": "Data consumed and persisted successfully."}, 200


if __name__ == '__main__':
    app.run(port=9000)
