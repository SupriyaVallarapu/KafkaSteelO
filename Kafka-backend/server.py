# from flask import Flask, request, jsonify
# from subprocess import Popen, PIPE

# app = Flask(__name__)

# @app.route('/api/process', methods=['POST'])
# def process_csv():
#     data_dir = request.json['data_dir']
#     kafka_broker = request.json['kafka_broker']
#     kafka_topic = request.json['kafka_topic']

#     command = ['python', 'Kafka_CSVFile_Data_Producer.py', data_dir, kafka_broker, kafka_topic]

#     process = Popen(command, stdout=PIPE, stderr=PIPE)
#     stdout, stderr = process.communicate()

#     if process.returncode != 0:
#         return jsonify({'error': 'An error occurred during processing'}), 500

#     return jsonify({'message': 'Processing completed'})

# if __name__ == '__main__':
#     app.run(debug=True)
