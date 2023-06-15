from flask import Flask
import subprocess
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/producer')
def producer():
    subprocess.Popen(['python', './Producers/Kafka_CSVFile_Data_Producer.py'])
    return "Producer script started", 200

@app.route('/consumer_persist')
def consumer_persist():
    subprocess.Popen(['python', './Database_Persist_only/Kafka_Database_Persist_Consumer.py'])
    return "Consumer persist script started", 200

if __name__ == "__main__":
    app.run(port=8080)
