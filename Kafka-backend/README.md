# Kafka Repo README
Welcome to sap156/Kafka repository! This repository hosts a collection of Python scripts and Docker Compose files aimed to help you interact with Apache Kafka, a leading open-source distributed event streaming platform.

# Table of Contents
1. Introduction
2. Prerequisites
3. Installation
4. Usage
5. Contributing
6. License

# Introduction
Apache Kafka is a robust event streaming platform that can process trillions of events daily. It offers low-latency, real-time handling and is used for a variety of applications such as data pipelines, analytics, data integration, and mission-critical applications.

This repository contains Python scripts demonstrating how to produce data to Kafka, consume data from Kafka, fetch server names, and topic names. In addition, this repository includes Docker Compose YAML files for setting up a Kafka environment.

# Prerequisites
To make the most out of this repository, you should have a basic understanding of:

1. Python programming
2. Apache Kafka
3. Docker and Docker Compose

# Installation
Before running the scripts or applications in this repository, ensure Apache Kafka and Docker are installed on your system.

Refer to the official documentation for installation guides:

1. Apache Kafka
2. Docker
3. Docker Compose

Afterward, clone this repository to your local machine: 
**git clone https://github.com/sap156/Kafka.git**

# Usage
The Python scripts in this repository demonstrate various interactions with Apache Kafka:

1. ***_Producer.py:** These scripts produces data to a specified Kafka topic.
2. ***_Persist_and_Produce.py:** These scripts produces data to a specified Kafka topic and/or persist data to PostgresSQL.
3. **Kafka_Consumer_Test.py:** This script consumes data from a specified Kafka topic.
4. **Kafka_Test_Connection.py:** This script tests connection to your Kafka cluster and fetches Kafka server names.
5. **List_Kafka_Topics.py:** This script fetches Kafka topic names.
6. **Kafka_Create_Topic.py:** This script will create a new Kafka topic with desired partition and replication factor.

Before running any script, make sure that your Kafka server is up and running.

The Docker Compose files define services, networks, and volumes for a Kafka deployment. You can use them as-is or modify them according to your needs. To run a Docker Compose file:

**docker-compose -f <docker-compose-file.yml> up -d**

Remember to replace <docker-compose-file.yml> with the actual file name.

# **Contributing**


# **License**




