# import json
# from flask import Blueprint, Flask, Response, jsonify, request, abort
# from confluent_kafka import Consumer, TopicPartition

# get_partitions_blueprint = Blueprint('get_partitions_blueprint', __name__)

# def consume_messages_partitions(consumer_config, topic, partition_nums):
#     consumer = Consumer(consumer_config)
#     partitions = consumer.list_topics(topic).topics[topic].partitions

#     partition_ids = []
#     for partition_num in partition_nums:
#         if not partition_num.isdigit():
#             abort(400, 'Invalid partition numbers.')
#         partition_id = int(partition_num)
#         if partition_id not in partitions.keys():
#             abort(400, f"Invalid partition number: {partition_id}")
#         partition_ids.append(partition_id)

#     topic_partitions = [TopicPartition(topic, partition_id) for partition_id in partition_ids]
#     consumer.assign(topic_partitions)

#     messages = []

#     while True:
#         msg = consumer.poll(1.0)
#         if msg is None:
#             break
#         if msg.error():
#             print("Error: {}".format(msg.error()))
#             continue

#         message = msg.value().decode('utf-8')
#         messages.append(json.loads(message))

#     consumer.close()

#     return messages

# @get_partitions_blueprint.route('/get_partitions/<partition_nums>/<offset>/<topic>/<group_id>', methods=['GET'])
# def get_partition_messages(partition_nums, offset, topic, group_id):
#     # Validate inputs
#     if not partition_nums or not offset or not topic or not group_id:
#         abort(400, 'Missing required parameters.')

#     partition_nums = partition_nums.split(',')
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
#         messages = consume_messages_partitions(consumer_config, topic, partition_nums)
#         return jsonify(messages)
#     except Exception as e:
#         abort(500, 'An error occurred while consuming messages.')

# # @get_partitions_blueprint.errorhandler(400)
# # def bad_request(error):
# #     response = jsonify({'error': error.description})
# #     response.status_code = 400
# #     return response

# # @get_partitions_blueprint.errorhandler(404)
# # def not_found(error):
# #     response = jsonify({'error': error.description})
# #     response.status_code = 404
# #     return response

# # @get_partitions_blueprint.errorhandler(500)
# # def internal_server_error(error):
# #     response = jsonify({'error': error.description})
# #     response.status_code = 500
# #     return response

# # if __name__ == '__main__':
# #     app.run(port=3002)


import json
from flask import Blueprint, Flask, Response, jsonify, request, abort
from confluent_kafka import Consumer, TopicPartition

get_partitions_blueprint = Blueprint('get_partitions_blueprint', __name__)

def consume_messages_partitions(consumer_config, topic, partition_nums):
    consumer = Consumer(consumer_config)
    partitions = consumer.list_topics(topic).topics[topic].partitions

    partition_ids = []
    for partition_num in partition_nums:
        if not partition_num.isdigit():
            abort(400, 'Invalid partition numbers.')
        partition_id = int(partition_num)
        if partition_id not in partitions.keys():
            abort(400, f"Invalid partition number: {partition_id}")
        partition_ids.append(partition_id)

    topic_partitions = [TopicPartition(topic, partition_id) for partition_id in partition_ids]
    consumer.assign(topic_partitions)

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Error: {}".format(msg.error()))
            continue

        message = msg.value().decode('utf-8')
        yield 'data: %s\n\n' % json.dumps(json.loads(message))

@get_partitions_blueprint.route('/get_partitions/<partition_nums>/<offset>/<topic>/<group_id>', methods=['GET'])
def get_partition_messages(partition_nums, offset, topic, group_id):
    # Validate inputs
    if not partition_nums or not offset or not topic or not group_id:
        abort(400, 'Missing required parameters.')

    partition_nums = partition_nums.split(',')
    offset = offset.lower()
    if offset not in ['earliest', 'latest']:
        abort(400, 'Invalid offset.')

    consumer_config = {
        'bootstrap.servers': 'kafka1:19092',
        'group.id': group_id,
        'auto.offset.reset': offset,
        'enable.auto.commit': False
    }

    return Response(consume_messages_partitions(consumer_config, topic, partition_nums), mimetype='text/event-stream')

# if __name__ == '__main__':
#     app.run(port=3002)
