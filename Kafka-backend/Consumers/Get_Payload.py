# import json
# from flask import Blueprint, Flask, Response, abort
# from confluent_kafka import Consumer, TopicPartition

# get_payload_blueprint = Blueprint('get_payload_blueprint', __name__)


# def consume_messages_all(consumer_config, topic):
#     consumer = Consumer(consumer_config)
#     messages = []
#     topics = consumer.list_topics().topics
#     if topic not in topics:
#                 raise Exception("Topic '{}' does not exist".format(topic))

#     # Get the list of partitions for the topic
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
#         payload = json.loads(message)['payload']  # Extract 'payload' from the JSON message
#         messages.append(payload)

#     consumer.close()

#     return messages

# @get_payload_blueprint.route('/get/payload/<offset>/<topic>/<group_id>', methods=['GET'])
# def get_all_messages(offset, topic, group_id):
#     # Validate inputs
#     if not offset or not topic or not group_id:
#         abort(400, 'Missing required parameters.')

#     offset = offset.lower()
#     if offset not in ['earliest', 'latest']:
#         abort(400, 'Invalid offset.')

#     consumer_config = {
#         'bootstrap.servers': 'kafka1:19092',
#         'group.id': group_id,
#         'auto.offset.reset': offset,
#         'enable.auto.commit': False
#     }

#     try:
#         messages = consume_messages_all(consumer_config, topic)
#         json_data = json.dumps(messages)  # Convert Python list to JSON string
#         return Response(json_data, mimetype='application/json')
#     except Exception as e:
#         abort(500, 'An error occurred while consuming messages.')

# # @get_payload_blueprint.errorhandler(400)
# # def bad_request(error):
# #     response = Response(json.dumps({'error': error.description}), mimetype='application/json')
# #     response.status_code = 400
# #     return response

# # @get_payload_blueprint.errorhandler(500)
# # def internal_server_error(error):
# #     response = Response(json.dumps({'error': error.description}), mimetype='application/json')
# #     response.status_code = 500
# #     return response

# # if __name__ == '__main__':
# #     app.run(port=3002)

# import json
# from flask import Blueprint, Flask, Response, abort
# from confluent_kafka import Consumer, TopicPartition

# get_payload_blueprint = Blueprint('get_payload_blueprint', __name__)

# def consume_messages_all(consumer_config, topic):
#     consumer = Consumer(consumer_config)
#     topics = consumer.list_topics().topics
#     if topic not in topics:
#         raise Exception("Topic '{}' does not exist".format(topic))

#     # Get the list of partitions for the topic
#     partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
#     consumer.assign([TopicPartition(topic, partition) for partition in partitions])

#     no_message_count = 0
#     max_no_message_count = 100  # 100 * 1.0 seconds = 100 seconds wait in worst case

#     while True:
#         msg = consumer.poll(1.0)
#         if msg is None:
#             no_message_count += 1
#             if no_message_count > max_no_message_count:
#                 break  # Leave while loop after max retries
#             continue
#         else:
#             no_message_count = 0

#         if msg.error():
#             print("Error: {}".format(msg.error()))
#             continue

#         message = msg.value().decode('utf-8')
#         payload = json.loads(message)['payload']  # Extract 'payload' from the JSON message
#         yield json.dumps(payload) + '\n'

#     consumer.close()

# @get_payload_blueprint.route('/get/payload/<offset>/<topic>/<group_id>', methods=['GET'])
# def get_all_messages(offset, topic, group_id):
#     # Validate inputs
#     if not offset or not topic or not group_id:
#         abort(400, 'Missing required parameters.')

#     offset = offset.lower()
#     if offset not in ['earliest', 'latest']:
#         abort(400, 'Invalid offset.')

#     consumer_config = {
#         'bootstrap.servers': 'kafka1:19092',
#         'group.id': group_id,
#         'auto.offset.reset': offset,
#         'enable.auto.commit': False
#     }

#     try:
#         return Response(consume_messages_all(consumer_config, topic), mimetype='application/json')
#     except Exception as e:
#         abort(500, 'An error occurred while consuming messages.')

import json
from flask import Blueprint, Flask, Response, abort
from confluent_kafka import Consumer, TopicPartition

get_payload_blueprint = Blueprint('get_payload_blueprint', __name__)

def consume_messages_all(consumer_config, topic):
    consumer = Consumer(consumer_config)
    topics = consumer.list_topics().topics
    if topic not in topics:
        raise Exception("Topic '{}' does not exist".format(topic))

    partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
    consumer.assign([TopicPartition(topic, partition) for partition in partitions])

    no_message_count = 0
    max_no_message_count = 100

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            no_message_count += 1
            if no_message_count > max_no_message_count:
                break
            continue
        else:
            no_message_count = 0

        if msg.error():
            print("Error: {}".format(msg.error()))
            continue

        message = msg.value().decode('utf-8')
        payload = json.loads(message)['payload']
        yield f'data: {json.dumps(payload)}\n\n'

    consumer.close()

@get_payload_blueprint.route('/get/payload/<offset>/<topic>/<group_id>', methods=['GET'])
def get_all_messages(offset, topic, group_id):
    if not offset or not topic or not group_id:
        abort(400, 'Missing required parameters.')

    offset = offset.lower()
    if offset not in ['earliest', 'latest']:
        abort(400, 'Invalid offset.')

    consumer_config = {
        'bootstrap.servers': 'kafka1:19092',
        'group.id': group_id,
        'auto.offset.reset': offset,
        'enable.auto.commit': False
    }

    try:
        return Response(consume_messages_all(consumer_config, topic), mimetype='text/event-stream')
    except Exception as e:
        abort(500, 'An error occurred while consuming messages.')
