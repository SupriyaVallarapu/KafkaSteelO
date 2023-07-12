from flask import Blueprint, Response, jsonify
from confluent_kafka import Consumer, KafkaException, TopicPartition
import json
from werkzeug.exceptions import BadRequest

get_schema_blueprint = Blueprint('get_schema_blueprint', __name__)

def consume_latest_message(consumer_config, topic):
    consumer = Consumer(consumer_config)
    latest_message = None

    try:
        partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
        if not partitions:
            raise BadRequest(f"No partitions found for topic: {topic}")

        last_partition = max(partitions)
        consumer.assign([TopicPartition(topic, last_partition)])

        # Get the end offset of the partition
        end_offset = consumer.get_watermark_offsets(TopicPartition(topic, last_partition))[1]
        if end_offset == 0:
            # No messages available in the partition
            raise BadRequest(f"No messages available in topic: {topic}")

        # Fetch the last message
        consumer.seek(TopicPartition(topic, last_partition, end_offset - 1))
        msg = consumer.poll(10.0)

        if msg is not None and not msg.error():
            message = msg.value().decode('utf-8')
            latest_message = json.loads(message)['schema']

    except KafkaException as ke:
        raise BadRequest(f"KafkaException: {ke}")

    except Exception as e:
        raise BadRequest(f"Exception: {e}")

    finally:
        consumer.close()

    return latest_message

@get_schema_blueprint.route('/get/schema/<topic>/<group_id>', methods=['GET'])
def get_latest_message_schema(topic, group_id):
    consumer_config = {
        'bootstrap.servers': 'kafka1:19092',
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False
    }

    try:
        latest_message_schema = consume_latest_message(consumer_config, topic)
        if latest_message_schema:
            fields = latest_message_schema['fields']
            reduced_schema = [{'field': field['field'], 'type': field['type']} for field in fields]
            return jsonify(reduced_schema)
        else:
            return Response(status=404)

    except BadRequest as e:
        return Response(str(e), status=400)

    except Exception as e:
        return Response(f"Internal Server Error: {e}", status=500)
