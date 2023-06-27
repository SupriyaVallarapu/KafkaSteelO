
# Introduction


The Cassandra Connector is a high speed mechanism for writing data to `Apache Cassandra
<http://cassandra.apache.org/>`_.



# Sink Connectors


## Cassandra Sink Connector

The Cassandra Sink connector is used to write data to a Cassandra Cluster. This connector works by utilizing the `Batch <http://docs.datastax.com/en/drivers/java/3.0/com/datastax/driver/core/querybuilder/Batch.html>`_ functionality to write all of the records in each poll in a single batch.

### Important

This connector can be configured to manage the schema on the Cassandra cluster. When altering an existing table the key is ignored. This is due to the potential issues changing a primary key on an existing table. The key schema is used to generate a primary key for the table when it is newly created. These fields must be in the value schema as well. Data written to the table is always read from the value from Kafka. This connector uses the topic to determine the name of the table to write to. This can be changed on the fly by using a transform to change the topic name.
### Note

This connector uses the topic to determine the name of the table to write to. This can be changed on the fly by using a transform like `Regex Router <https://kafka.apache.org/documentation/#connect_transforms>`_ to change the topic name.
### Tip

If you encounter error messages like this `Batch for [test.twitter] is of size 127.661KiB, exceeding specified threshold of 50.000KiB by 77.661KiB.` or warning messages like `Batch for [test.twitter] is of size 25.885KiB, exceeding specified threshold of 5.000KiB by 20.885KiB.` Try adjusting the `consumer.max.poll.records` setting in the worker.properties for Kafka Connect.


### Configuration

#### Connection


##### `cassandra.contact.points`

The Cassandra hosts to connect to.

*Importance:* High

*Type:* List

*Default Value:* [localhost]



##### `cassandra.password`

The password to connect to Cassandra with.

*Importance:* High

*Type:* Password

*Default Value:* [hidden]



##### `cassandra.security.enabled`

Flag to determine if security is enabled.

*Importance:* High

*Type:* Boolean

*Default Value:* true



##### `cassandra.ssl.enabled`

Flag to determine if SSL is enabled when connecting to Cassandra.

*Importance:* High

*Type:* Boolean

*Default Value:* false



##### `cassandra.username`

The username to connect to Cassandra with.

*Importance:* High

*Type:* String

*Default Value:* cassandra



##### `cassandra.port`

The port the Cassandra hosts are listening on.

*Importance:* Medium

*Type:* Int

*Default Value:* 9042

*Validator:* ValidPort{start=1025, end=65535}



##### `cassandra.compression`

Compression algorithm to use when connecting to Cassandra.

*Importance:* Low

*Type:* String

*Default Value:* NONE

*Validator:* [NONE, SNAPPY, LZ4]


#### Keyspace


##### `cassandra.keyspace`

The keyspace to write to.

*Importance:* High

*Type:* String



##### `cassandra.keyspace.create.enabled`

Flag to determine if the keyspace should be created if it does not exist.

*Importance:* High

*Type:* Boolean

*Default Value:* true


#### SSL


##### `cassandra.ssl.truststore.password`

Password to open the Java Truststore with.

*Importance:* Medium

*Type:* Password

*Default Value:* [hidden]

*Validator:* com.github.jcustenborder.kafka.connect.cassandra.CassandraSinkConnectorConfig$BlankOrValidator@31cae1e4



##### `cassandra.ssl.truststore.path`

Path to the Java Truststore.

*Importance:* Medium

*Type:* String

*Validator:* com.github.jcustenborder.kafka.connect.cassandra.CassandraSinkConnectorConfig$BlankOrValidator@5280e62e



##### `cassandra.ssl.provider`

The SSL Provider to use when connecting to Cassandra

*Importance:* Low

*Type:* String

*Default Value:* JDK

*Validator:* ValidEnum{enum=SslProvider, allowed=[JDK, OPENSSL, OPENSSL_REFCNT]}


#### Table


##### `cassandra.table.manage.enabled`

Flag to determine if the connector should manage the table.

*Importance:* High

*Type:* Boolean

*Default Value:* true



##### `cassandra.table.create.caching`

Caching setting to use.

*Importance:* Medium

*Type:* String

*Default Value:* NONE

*Validator:* ValidEnum{enum=Caching, allowed=[ALL, KEYS_ONLY, ROWS_ONLY, NONE]}



##### `cassandra.table.create.compression.algorithm`

Compression algorithm to use when the table is created.

*Importance:* Medium

*Type:* String

*Default Value:* NONE

*Validator:* [NONE, SNAPPY, LZ4, DEFLATE]


#### Write


##### `cassandra.consistency.level`

The requested consistency level to use when writing to Cassandra.

*Importance:* High

*Type:* String

*Default Value:* LOCAL_QUORUM

*Validator:* ValidEnum{enum=ConsistencyLevel, allowed=[ANY, ONE, TWO, THREE, QUORUM, ALL, LOCAL_QUORUM, EACH_QUORUM, SERIAL, LOCAL_SERIAL, LOCAL_ONE]}



##### `cassandra.deletes.enabled`

Flag to determine if the connector should process deletes.

*Importance:* High

*Type:* Boolean

*Default Value:* true



##### `cassandra.write.mode`

The type of statement to build when writing to Cassandra.

*Importance:* High

*Type:* String

*Default Value:* Insert



#### Examples

##### Standalone Example

This configuration is used typically along with [standalone mode](http://docs.confluent.io/current/connect/concepts.html#standalone-workers).

```properties
name=CassandraSinkConnector1
connector.class=com.github.jcustenborder.kafka.connect.cassandra.CassandraSinkConnector
tasks.max=1
topics=< Required Configuration >
cassandra.keyspace=< Required Configuration >
```

##### Distributed Example

This configuration is used typically along with [distributed mode](http://docs.confluent.io/current/connect/concepts.html#distributed-workers).
Write the following json to `connector.json`, configure all of the required values, and use the command below to
post the configuration to one the distributed connect worker(s).

```json
{
  "config" : {
    "name" : "CassandraSinkConnector1",
    "connector.class" : "com.github.jcustenborder.kafka.connect.cassandra.CassandraSinkConnector",
    "tasks.max" : "1",
    "topics" : "< Required Configuration >",
    "cassandra.keyspace" : "< Required Configuration >"
  }
}
```

Use curl to post the configuration to one of the Kafka Connect Workers. Change `http://localhost:8083/` the the endpoint of
one of your Kafka Connect worker(s).

Create a new instance.
```bash
curl -s -X POST -H 'Content-Type: application/json' --data @connector.json http://localhost:8083/connectors
```

Update an existing instance.
```bash
curl -s -X PUT -H 'Content-Type: application/json' --data @connector.json http://localhost:8083/connectors/TestSinkConnector1/config
```



