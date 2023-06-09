from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType, StringType
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

spark = SparkSession.builder.appName("Log Monitor").getOrCreate()

# Define the UDF to search for 'ERROR' keyword
@udf(returnType=BooleanType())
def contains_error(line):
    line_json = json.loads(line)
    return 'ERROR' in line_json['log_line']

# Send email alert
@udf(returnType=StringType())
def send_email_alert(line):
    error_line = json.loads(line)['log_line']
    
    # Email content
    msg = MIMEMultipart()
    msg['From'] = 'neni.abhinav@gmail.com'
    msg['To'] = 'neni.abhinav@gmail.com'
    msg['Subject'] = 'Log Monitor Alert'
    message = f'ERROR found: {error_line}'
    msg.attach(MIMEText(message))

    # Send the email
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('your-email@gmail.com', 'your-password')
    mailserver.sendmail('your-email@gmail.com', 'receiver-email@gmail.com', msg.as_string())
    mailserver.quit()

    return 'Email Alert sent.'

# Subscribe to Kafka topic
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "log-topic").load()

# Filter the lines that contain 'ERROR'
errorLines = df.filter(contains_error(col("value")))

# Send email alerts
alert = errorLines.withColumn("Alert", send_email_alert(col("value")))

# Write out the 'ERROR' lines and Alert status to console
query = alert.writeStream.outputMode("append").format("console").start()

query.awaitTermination()