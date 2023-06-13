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
from flask_cors import CORS
import time
from confluent_kafka import Consumer, KafkaError
import json
import psycopg2
from getpass import getpass

app = Flask(__name__)
cors=CORS(app)
@app.route('/api/consume_kafka', methods=['POST'])
def consume_kafka():
    # Get the JSON body of the request
    request_body = request.json

    # Get the parameters from the JSON body
    data_source = request_body.get('data_source')
    kafka_broker = request_body.get('kafka_broker', "localhost:9092")
    kafka_topic = request_body.get('kafka_topic')
    offset = request_body.get('offset', "end")
    persist_data = request_body.get('persist_data', "no")
    consumer_group = request_body.get('consumer_group', "testgroup")

    db_name = request_body.get('db_name', "kafka")
    db_schema = request_body.get('db_schema', "kafkadata")
    db_user = request_body.get('db_user', "postgres")
    db_password = request_body.get('db_password', "postgres")
    db_host = request_body.get('db_host', "localhost")
    db_port = request_body.get('db_port', "5432")

    # Create a consumer to consume data from Kafka
    consumer = Consumer({
        'bootstrap.servers': kafka_broker,
        'group.id': consumer_group,
        'auto.offset.reset': offset
    })

    consumer.subscribe([kafka_topic])


    def persist_to_timescaleDB(message, cur, conn):
        # Serialize the message to JSON
        message_json = json.dumps(message)

        # Persist the data to TimescaleDB
        cur.execute(
            f"INSERT INTO {db_schema}.{kafka_topic} (data) VALUES (%s)",
            (message_json,)
        )
        conn.commit()

    conn = None
    cur = None
    try:
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
                    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    data JSONB
                );
            """)
            conn.commit()

        # Consume data from the Kafka topic
        message = consumer.poll(1.0)

        # if a message is received
        if message is not None:
            # if the message does not contain error
            if message.error() is None:
                message = json.loads(message.value().decode('utf-8'))

                # Persist the data to TimescaleDB
                persist_to_timescaleDB(message, cur, conn)
            elif message.error().code() != KafkaError._PARTITION_EOF:
                return {"error": f"Error occurred: {message.error()}"}, 500
                if conn:
                    conn.close()
                time.sleep(1)

    except Exception as e:
        return {"error": f"Error occurred: {e}"}, 500
        if conn:
            conn.close()
        time.sleep(10)

    return {"message": "Data consumed and persisted successfully."}, 200
if __name__ == '__main__':
    app.run(port=8080)
