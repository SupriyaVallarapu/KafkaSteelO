from flask import Flask, request,Blueprint
from flask_cors import CORS,cross_origin
from confluent_kafka import Consumer, TopicPartition, KafkaError
import json
import psycopg2
from getpass import getpass
import traceback

persist_blueprint= Blueprint('persist_blueprint', __name__)
@persist_blueprint.route('/api/consume_and_persist', methods=['POST'])
@cross_origin()
def consume_and_persist():
    try:
        # Get the JSON body of the request
        request_body = request.json
    except Exception:
        return {"error": "Error parsing request body"}, 400

    try:
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
    except Exception:
        return {"error": "Error getting parameters from request body"}, 400

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
    except psycopg2.Error as e:
        return {"error": f"Error connecting to database: {str(e)}"}, 500

    try:
        # Create a table for the Kafka topic if it doesn't exist
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_schema}.{kafka_topic} (
                timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                data JSONB
            );
        """)
        conn.commit()
    except psycopg2.Error as e:
        return {"error": f"Error creating table: {str(e)}"}, 500

    try:
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
