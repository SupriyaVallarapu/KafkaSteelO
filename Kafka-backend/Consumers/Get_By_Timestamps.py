# from flask import Blueprint, Flask, Response, jsonify
# from confluent_kafka import Consumer, TopicPartition
# import json
# from datetime import datetime

# get_by_timestamp_blueprint = Blueprint('get_by_timestamp_blueprint', __name__)


# def consume_messages_all(consumer_config, topic):
#     consumer = Consumer(consumer_config)
#     messages = []

#     partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
#     consumer.assign([TopicPartition(topic, partition) for partition in partitions])

#     while True:
#         msg = consumer.poll(1.0)
#         if msg is None:
#             break
#         if msg.error():
#             print("Error: {}".format(msg.error()))
#             continue

#         message = msg.value().decode('utf-8')
#         messages.append(message)

#     consumer.close()

#     return messages


# def search_messages_by_time_range(messages, start_time, end_time):
#     found_messages = []

#     for message in messages:
#         try:
#             message_dict = json.loads(message)
#             if 'timestamp' in message_dict:
#                 timestamp = datetime.fromisoformat(message_dict['timestamp'])
#                 if start_time <= timestamp <= end_time:
#                     found_messages.append(message_dict)
#         except json.JSONDecodeError:
#             print("Invalid JSON message:", message)

#     return found_messages


# @get_by_timestamp_blueprint.route('/get/time-range/<offset>/<topic>/<group_id>/<start_time>/<end_time>', methods=['GET'])
# def get_messages_by_time_range(offset, topic, group_id, start_time, end_time):
#     try:
#         start_time = datetime.fromisoformat(start_time)
#         end_time = datetime.fromisoformat(end_time)
#     except ValueError:
#         error_message = "Invalid start_time or end_time. Please provide timestamps in ISO 8601 format."
#         return jsonify({'error': error_message}), 400

#     consumer_config = {
#         'bootstrap.servers': 'kafka1:19092',
#         'group.id': group_id,
#         'auto.offset.reset': offset,
#         'enable.auto.commit': False
#     }

#     try:
#         messages = consume_messages_all(consumer_config, topic)
#         found_messages = search_messages_by_time_range(messages, start_time, end_time)

#         json_data = json.dumps(found_messages)
#         return Response(json_data, mimetype='application/json')

#     except Exception as e:
#         error_message = str(e)
#         return jsonify({'error': error_message}), 500


# # if __name__ == '__main__':
# #     app.run(port=3002)

from flask import Blueprint, Flask, Response, jsonify
from confluent_kafka import Consumer, TopicPartition
import json
from datetime import datetime

get_by_timestamp_blueprint = Blueprint('get_by_timestamp_blueprint', __name__)

@get_by_timestamp_blueprint.route('/get/time-range/<offset>/<topic>/<group_id>/<start_time>/<end_time>', methods=['GET'])
def get_messages_by_time_range(offset, topic, group_id, start_time, end_time):
    consumer_config = {
        'bootstrap.servers': 'kafka1:19092',
        'group.id': group_id,
        'auto.offset.reset': offset,
        'enable.auto.commit': False
    }

    try:
        # Validate and parse start_time and end_time as datetime objects
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)

        def generate():
            consumer = Consumer(consumer_config)

            # Check if the topic exists
            topics = consumer.list_topics().topics
            if topic not in topics:
                raise Exception("Topic '{}' does not exist".format(topic))

            # Get the list of partitions for the topic
            partitions = topics[topic].partitions.keys()
            consumer.assign([TopicPartition(topic, partition) for partition in partitions])

            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    raise Exception("Kafka error: {}".format(msg.error()))

                message = msg.value().decode('utf-8')
                message_dict = json.loads(message)

                # Check if the message timestamp is within the start_time and end_time
                if 'timestamp' in message_dict:
                    timestamp = datetime.fromisoformat(message_dict['timestamp'])
                    if start_time <= timestamp <= end_time:
                        yield 'data: %s\n\n' % json.dumps(message_dict)

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        return jsonify(error="Failed to retrieve messages: {}".format(str(e))), 500
