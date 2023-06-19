import threading
import os
from flask import Flask
from flask_cors import CORS
from Producers.Kafka_CSVFile_Data_Producer import csv_blueprint
from Producers.Kafka_API_Data_Producer import api_blueprint
from Producers.Kafka_ParquetFile_Data_Producer import parquet_blueprint
from Database_Persist_only.Kafka_Database_Persist_Consumer import persist_blueprint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://localhost:3000"]}})

app.register_blueprint(csv_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(parquet_blueprint)
app.register_blueprint(persist_blueprint)


if __name__ == "__main__":
    app.run(port=8080)

# def run_app(cmd):
#     os.system(cmd)

# if __name__ == "__main__":
#     producer_command = "python Producers/Kafka_CSVFile_Data_Producer.py"
#     # producer_command1 = "python Producers/Kafka_API_Data_Producer.py"
#     consumer_command = "python Database_Persist_only/Kafka_Database_Persist_Consumer.py"
    
#     # Create threads
#     producer_thread = threading.Thread(target=run_app, args=(producer_command,))
#     # producer_thread1 = threading.Thread(target=run_app, args=(producer_command1,))

#     consumer_thread = threading.Thread(target=run_app, args=(consumer_command,))

#     # Start threads
#     producer_thread.start()
#     # producer_thread1.start()
#     consumer_thread.start()


#     producer_thread.join()
#     # producer_thread1.join()
#     consumer_thread.join()
#     # Wait for both threads to finish

 
