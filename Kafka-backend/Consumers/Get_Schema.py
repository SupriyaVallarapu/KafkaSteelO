import json
from flask import Blueprint, Flask, Response
from confluent_kafka import Consumer, KafkaException, TopicPartition

get_schema_blueprint = Blueprint('get_schema_blueprint', __name__)
def consume_latest_message(consumer_config, topic):
    consumer = Consumer(consumer_config)

    try:
        # Get the last partition for the topic
        partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
        last_partition = max(partitions)
        consumer.assign([TopicPartition(topic, last_partition)])

        # Get the last offset in the partition
        end_offset = consumer.get_watermark_offsets(TopicPartition(topic, last_partition))[1]
        last_offset = end_offset - 1

        latest_message = None

        if last_offset >= 0:
            # Seek to the last offset and fetch the message
            consumer.seek(TopicPartition(topic, last_partition, last_offset))
            msg = consumer.poll(5.0)

            if msg is not None and not msg.error():
                message = msg.value().decode('utf-8')
                fields = json.loads(message)['schema']['fields']
                extracted_fields = [{'type': field['type'], 'field': field['field']} for field in fields]
                latest_message = extracted_fields

    except KafkaException as ke:
        # Handle Kafka-related exceptions
        print(f"KafkaException: {ke}")

    except Exception as e:
        # Handle other exceptions
        print(f"Exception: {e}")

    finally:
        consumer.close()

    return latest_message

@get_schema_blueprint.route('/get/schema/<topic>/<group_id>', methods=['GET'])
def get_latest_message_schema(topic, group_id):
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': group_id,
        'auto.offset.reset': 'latest',
        'enable.auto.commit': False
    }

    latest_message_schema = consume_latest_message(consumer_config, topic)
    if latest_message_schema:
        json_data = json.dumps(latest_message_schema)
        return Response(json_data, mimetype='application/json')
    else:
        return Response(status=404)

# if __name__ == '__main__':
#     app.run(port=3002)
