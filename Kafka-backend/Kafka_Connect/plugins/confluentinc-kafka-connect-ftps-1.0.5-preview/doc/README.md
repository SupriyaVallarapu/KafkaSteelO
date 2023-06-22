# Introduction

This project provides connectors for Kafka Connect to read and write data to Ftps.

# Documentation

Documentation on the connector is hosted on Confluent's
[docs site](https://docs.confluent.io/current/connect/kafka-connect-ftps/).

Source code is located in Confluent's
[docs repo](https://github.com/confluentinc/docs/tree/master/connect/kafka-connect-ftps). If changes
are made to configuration options for the connector, be sure to generate the RST docs (as described
below) and open a PR against the docs repo to publish those changes!

# Configs

Documentation on the configurations for each connector can be automatically generated via Maven.

To generate documentation for the sink connector:
```bash
mvn -Pdocs exec:java@sink-config-docs
```

To generate documentation for the source connector:
```bash
mvn -Pdocs exec:java@source-config-docs
```

# Compatibility Matrix:

This connector has been tested against the following versions of Apache Kafka
and Ftps:

|                          | AK 1.0             | AK 1.1        | AK 2.0        |
| ------------------------ | ------------------ | ------------- | ------------- |
| **Ftps v1.2.3** | NOT COMPATIBLE (1) | OK            | OK            |

1. The connector needs header support in Connect.

# Setting up an FTPS server 
* docker run -d \\\
   -p 20:20 -p 21:21 -p 21100-21110:21100-21110 \\\
   -e FTP_USER=myuser -e FTP_PASS=mypass \\\
   -e PASV_ADDRESS=127.0.0.1 -e PASV_MIN_PORT=21100 -e PASV_MAX_PORT=21110 \\\
   --name vsftpd --restart=always fauria/vsftpd
* Run `docker exec -i -t vsftpd bash` to ssh into the Docker container.
* Add the following lines to `/etc/vsftpd/vsftpd.conf` : 
```
rsa_cert_file=/etc/ssl/private/vsftpd.pem
rsa_private_key_file=/etc/ssl/private/vsftpd.pem
ssl_enable=YES
allow_anon_ssl=NO
force_local_data_ssl=YES
force_local_logins_ssl=YES
ssl_tlsv1=YES
ssl_sslv2=NO
ssl_sslv3=NO
require_ssl_reuse=NO

```
* Add all required files and directories that need to be served, into `/home/vsftpd/myuser/` 
* Exit the container.
* Copy the `vsftpd.pem` file in the `test/docker/configA` folder using `docker cp test/docker
/configA/vsftp.pem vsftpd:/etc/ssl/private/`
* Run `docker restart vsftpd` 
* The FTPS server is ready to use at 127.0.0.1 , port 21 with `myuser` and `mypass` as the
 username and password respectively. 