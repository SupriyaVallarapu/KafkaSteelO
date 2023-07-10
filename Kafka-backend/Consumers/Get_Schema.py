import json
from flask import Blueprint, Flask, Response
from confluent_kafka import Consumer, KafkaException, TopicPartition

get_schema_blueprint = Blueprint('get_schema_blueprint', __name__)

# def consume_latest_message(consumer_config, topic):
#     consumer = Consumer(consumer_config)

#     try:
#         # Get the partitions for the topic
#         partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
#         num_partitions = len(partitions)

#         if num_partitions == 1:
#             # If there is only one partition, take the last offset of that partition
#             partition = partitions[0]
#             consumer.assign([TopicPartition(topic, partition)])

#             end_offset = consumer.get_watermark_offsets(TopicPartition(topic, partition))[1]
#             last_offset = end_offset - 1

#         elif num_partitions > 1:
#             # If there are multiple partitions, follow the existing logic to find the last offset
#             last_partition = max(partitions)
#             consumer.assign([TopicPartition(topic, last_partition)])

#             end_offset = consumer.get_watermark_offsets(TopicPartition(topic, last_partition))[1]
#             last_offset = end_offset - 1

#         else:
#             # Handle the case where there are no partitions
#             return None

#         latest_message = None

#         if last_offset >= 0:
#             # Seek to the last offset and fetch the message
#             consumer.seek(TopicPartition(topic, partition, last_offset))
#             msg = consumer.poll(5.0)

#             if msg is not None and not msg.error():
#                 message = msg.value().decode('utf-8')
#                 fields = json.loads(message)['schema']['fields']
#                 extracted_fields = [{'type': field['type'], 'field': field['field']} for field in fields]
#                 latest_message = extracted_fields

#     except KafkaException as ke:
#         # Handle Kafka-related exceptions
#         print(f"KafkaException: {ke}")

#     except Exception as e:
#         # Handle other exceptions
#         print(f"Exception: {e}")

#     finally:
#         consumer.close()

#     return latest_message


# @get_schema_blueprint.route('/get/schema/<topic>/<group_id>', methods=['GET'])
# def get_latest_message_schema(topic, group_id):
#     consumer_config = {
#         'bootstrap.servers': 'kafka1:19092',
#         'group.id': group_id,
#         'auto.offset.reset': 'earliest',
#         'enable.auto.commit': False
#     }

#     latest_message_schema = consume_latest_message(consumer_config, topic)
#     if latest_message_schema:
#         json_data = json.dumps(latest_message_schema)
#         return Response(json_data, mimetype='application/json')
#     else:
#         return Response(status=404)


def consume_messages(consumer_config, topic):
    consumer = Consumer(consumer_config)

    try:
        # Assign all partitions of the topic to the consumer
        partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
        consumer.assign([TopicPartition(topic, p) for p in partitions])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                break
            if msg.error():
                print(f"Kafka Error: {msg.error()}")
                continue

            # Decode message and extract schema
            message = msg.value().decode('utf-8')
            fields = json.loads(message)['schema']['fields']
            extracted_fields = [{'type': field['type'], 'field': field['field']} for field in fields]
            
            # Yield schema of the current message
            yield f'data: {json.dumps(extracted_fields)}\n\n'

    except KafkaException as ke:
        print(f"KafkaException: {ke}")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        consumer.close()


@get_schema_blueprint.route('/get/schema/<topic>/<group_id>', methods=['GET'])
def get_messages_schema(topic, group_id):
    consumer_config = {
        'bootstrap.servers': 'kafka1:19092',
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False
    }

    try:
        return Response(consume_messages(consumer_config, topic), mimetype='text/event-stream')
    except Exception as e:
        return {"error": str(e)}, 500
