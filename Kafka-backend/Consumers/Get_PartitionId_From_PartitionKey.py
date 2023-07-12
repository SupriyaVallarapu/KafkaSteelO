# import json
# from flask import Blueprint, Flask, Response, jsonify, abort
# from confluent_kafka import KafkaError, KafkaException, Consumer, TopicPartition
# from confluent_kafka.admin import AdminClient

# get_partitionid_from_partitionkey_blueprint = Blueprint('get_partitionid_from_partitionkey_blueprint', __name__)


# def get_partition_id(consumer_config, topic, partition_key):
#     try:
#         # Create a consumer to get partition information
#         consumer = Consumer(consumer_config)
#         partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
#         print(partitions)
#         consumer.assign([TopicPartition(topic, partition) for partition in partitions])
        
#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 break
#             if msg.error():
#                 print("Error: {}".format(msg.error()))
#                 continue

#             if msg.key() == partition_key.encode('utf-8'):
#                         consumer.close()
#                         return msg.partition()

#     except KafkaException as e:
#         print(f"Error while getting partition information: {str(e)}")

#     return None

# @get_partitionid_from_partitionkey_blueprint.route('/get_partition_id/<topic>/<partition_key>/<group_id>', methods=['GET'])
# def get_partition_id_endpoint(topic, partition_key, group_id):
#     # Validate inputs
#     if not topic or not partition_key or not group_id:
#         abort(400, 'Missing required parameters.')

#     consumer_config = {
#         'bootstrap.servers': 'kafka1:19092',
#         'group.id': group_id,
#         'auto.offset.reset': 'earliest',
#         'enable.auto.commit': False
#     }
#     partition_id = get_partition_id(consumer_config, topic, partition_key)

#     if partition_id is None:
#         abort(404, 'Partition not found.')

#     json_data = json.dumps(partition_id)
#     return Response(json_data, mimetype='application/json')


# # @get_partitionid_from_partitionkey_blueprint.errorhandler(400)
# # def bad_request(error):
# #     response = jsonify({'error': error.description})
# #     response.status_code = 400
# #     return response

# # @get_partitionid_from_partitionkey_blueprint.errorhandler(404)
# # def not_found(error):
# #     response = jsonify({'error': error.description})
# #     response.status_code = 404
# #     return response

# # if __name__ == '__main__':
# #     app.run(port=3002)



import json
from flask import Blueprint, Flask, Response, abort
from confluent_kafka import Consumer, KafkaException, TopicPartition

get_partitionid_from_partitionkey_blueprint = Blueprint('get_partitionid_from_partitionkey_blueprint', __name__)

def get_partition_id(consumer_config, topic, partition_key):
    try:
        # Create a consumer to get partition information
        consumer = Consumer(consumer_config)
        partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
        consumer.assign([TopicPartition(topic, partition) for partition in partitions])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Error: {}".format(msg.error()))
                continue

            if msg.key() == partition_key.encode('utf-8'):
                return msg.partition()

        consumer.close()

    except KafkaException as e:
        print(f"Error while getting partition information: {str(e)}")

    return None

@get_partitionid_from_partitionkey_blueprint.route('/get_partition_id/<topic>/<partition_key>/<group_id>', methods=['GET'])
def get_partition_id_endpoint(topic, partition_key, group_id):
    # Validate inputs
    if not topic or not partition_key or not group_id:
        abort(400, 'Missing required parameters.')

    consumer_config = {
        'bootstrap.servers': 'kafka1:19092',
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False
    }

    partition_id = get_partition_id(consumer_config, topic, partition_key)

    if partition_id is None:
        abort(404, 'Partition not found.')

    json_data = json.dumps(partition_id)
    return Response(json_data, mimetype='application/json')
