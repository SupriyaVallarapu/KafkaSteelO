# from flask import Blueprint, Flask, Response, jsonify
# from confluent_kafka import Consumer, KafkaException, TopicPartition
# import json
# from werkzeug.exceptions import BadRequest
# from datetime import datetime

# get_by_name_and_timestamps_blueprint = Blueprint('get_by_name_and_timestamps_blueprint', __name__)


# def consume_messages_all(consumer_config, topic):
#     consumer = Consumer(consumer_config)
#     messages = []

#     partitions = consumer.list_topics(topic).topics
#     topics = consumer.list_topics().topics
#     if topic not in topics:
#             raise Exception("Topic {} does not exist".format(topic))

#     partitions = partitions[topic].partitions.keys()
#     consumer.assign([TopicPartition(topic, partition) for partition in partitions])

#     try:
#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 break
#             if msg.error():
#                 raise KafkaException(msg.error())

#             message = msg.value().decode('utf-8')
#             messages.append(message)

#     except KafkaException as e:
#         raise BadRequest('An error occurred while consuming messages: {}'.format(str(e)))

#     finally:
#         consumer.close()

#     return messages


# def search_messages_by_time_range(messages, start_time, end_time):
#     found_messages = []

#     for message in messages:
#         try:
#             message_dict = json.loads(message)
#             if 'timestamp' in message_dict:
#                 timestamp = datetime.strptime(message_dict['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
#                 if start_time <= timestamp <= end_time:
#                     found_messages.append(message_dict)
#         except json.JSONDecodeError:
#             print("Invalid JSON message:", message)

#     return found_messages

# @get_by_name_and_timestamps_blueprint.route('/get/name-time-range/<offset>/<topic>/<group_id>/<start_time>/<end_time>/<name>', methods=['GET'])
# def get_messages_by_time_range(offset, topic, group_id, start_time, end_time, name):
#     try:
#         offset = offset.lower()
#         if offset not in ['earliest', 'latest']:
#             raise BadRequest('Invalid offset value. It should be either earliest or latest.')

#         topic = topic.lower()  # Convert topic to lowercase for consistency

#         # Validate and parse start_time and end_time as datetime objects
#         start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f')
#         end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f')

#         consumer_config = {
#             'bootstrap.servers': 'kafka1:19092',
#             'group.id': group_id,
#             'auto.offset.reset': offset,
#             'enable.auto.commit': False
#         }

#         messages = consume_messages_all(consumer_config, topic)
#         found_messages = search_messages_by_time_range(messages, start_time, end_time)

#         if name:
#             found_messages = [msg for msg in found_messages if msg.get('sensor_name') == name]

#         json_data = json.dumps(found_messages)
#         return Response(json_data, mimetype='application/json')

#     except ValueError:
#         raise BadRequest('Invalid date format. The date should be in the format "YYYY-MM-DDTHH:MM:SS.ssssss".')

#     except BadRequest as e:
#         raise e

#     except Exception as e:
#         raise BadRequest('An error occurred: {}'.format(str(e)))


# # if __name__ == '__main__':
# #     app.run(port=3002)


from flask import Blueprint, Flask, Response, jsonify
from confluent_kafka import Consumer, TopicPartition
import json
from datetime import datetime

get_by_name_and_timestamps_blueprint = Blueprint('get_by_name_and_timestamps_blueprint', __name__)

@get_by_name_and_timestamps_blueprint.route('/get/name-time-range/<offset>/<topic>/<group_id>/<start_time>/<end_time>/<name>', methods=['GET'])
def get_messages_by_time_range(offset, topic, group_id, start_time, end_time, name):
    consumer_config = {
        'bootstrap.servers': 'kafka1:19092',
        'group.id': group_id,
        'auto.offset.reset': offset,
        'enable.auto.commit': False
    }

    # Validate and parse start_time and end_time as datetime objects
    try:
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return jsonify(error="Invalid datetime format, should be 'YYYY-MM-DDTHH:MM:SS.ssssss'"), 400

    try:
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
                    timestamp = datetime.strptime(message_dict['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
                    if start_time <= timestamp <= end_time and message_dict.get('sensor_name') == name:
                        yield 'data: %s\n\n' % json.dumps(message_dict)

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        return jsonify(error="Failed to retrieve messages: {}".format(str(e))), 500
