import React, { useState } from 'react';
import '../styles/Filetypecsv.css';
import { Form, Button } from 'react-bootstrap';
import Layoutnavbar from '../Layouts/Layoutnavbar';
import { SuccessfulUploadAlert, FailedUploadAlert, EmptyFieldAlert } from '../Alerts/Alerts.js';
import '../styles/Dataconnector.css';
import Card from 'react-bootstrap/Card';

let id = 0;
function Dataconnectorform() {


    const jsonConfig =

    `{
    "connection.user": "username",
    "connection.password": "password",
    "name": "oracle_jdbc",
    "mode": "timestamp",
    "timestamp.column.name": "MODIFICATION_DATE",
    "key.converter.schemas.enable": "false",
    "topic.prefix": "oracle.kafka.oracldata.",
    "value.converter.schemas.enable": "false",
     For Oracle - 
    "connection.url": "jdbc:oracle:thin:@//10.172.251.67:1521/L3PROD" or
     For Postgres (within docker) - 
    "connection.url": "jdbc:postgresql://kafkasteelo-db-1:5432/postgres", or
     For MSSQL - 
    "connection.url": "jdbc:sqlserver://10.172.251.2:1433;databaseName=BRSDB",
    "table.whitelist": "CODES,DELAYS"
    }`;

    const [incrementingcolumnname, setincrementingcolumnname] = useState('');
    const [timestampColumnName, setTimestampColumnName] = useState('');
    const [connectionpassword, setconnectionpassword] = useState('');
    const [keyconverterschemasenable, setkeyconverterschemasenableKafkaTopic] = useState('');
    const [topicprefix, settopicprefix] = useState('');
    const [connectionuser, setconnectionuser] = useState('');
    const [valueconverterschemasenable, setvalueconverterschemasenable] = useState('');
    const [name, setname] = useState('');
    const [mode, setMode] = useState('');
    const [connectionurl, setconnectionurl] = useState('');
    const [tableincludelist, settableincludelist] = useState('');
    const [alerts, setAlerts] = useState([]);
    //const [connectorType, setConnectorType] = useState('postgres');  // Default to postgres



    const addAlert = (component) => {
        setAlerts(alerts => [...alerts, { id: id++, component }]);
    };

    const removeAlert = (id) => {
        setAlerts(alerts => alerts.filter(alert => alert.id !== id));
    };


    const handleSubmit = (e) => {
        e.preventDefault();

        setAlerts([]);  // Clear previous alerts


        // Validate fields
        if (!connectionpassword ||
            !keyconverterschemasenable || !topicprefix ||
            !connectionuser || !valueconverterschemasenable ||
            !name || !connectionurl || !tableincludelist) {
            addAlert(<EmptyFieldAlert />);
            return;
        }

        const payload = {
            // db_type: connectorType,
            incrementing_column_name: incrementingcolumnname,
            timestamp_column_name: timestampColumnName,
            connection_password: connectionpassword,
            mode: mode,
            key_converter_schemas_enable: keyconverterschemasenable,
            topic_prefix: topicprefix,
            connection_user: connectionuser,
            value_converter_schemas_enable: valueconverterschemasenable,
            name: name,
            connection_url: connectionurl,
            table_include_list: tableincludelist

        };

        fetch(`http://localhost:8080/api/dataconnector`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response.ok) {
                    return response.json();

                } else {
                    throw response;
                }
            })
            .then(data => {
                addAlert(<SuccessfulUploadAlert />);
            })

            // In case of a network failure or other kind of request failure
            .catch(error => {
                if (error.message === 'Internal Server Error') {
                    // We already added a URL alert, so just log the error
                    console.error(error.message);
                } else {
                    // Other errors
                    console.error('An error occurred:', error);
                    addAlert(<FailedUploadAlert />);
                }
            });
    };

    return (
        <Layoutnavbar>
            {alerts.map(({ id, component }) => React.cloneElement(component, { key: id, onClose: () => removeAlert(id) }))}
            <Card className='instructions-container'>
                <Card.Body>
                    <div >
                        <h3>Instructions</h3>
                        <br></br>
                        <ul>
                            <li>All fields marked * are mandatory</li>
                            <li>Following configuration can be used for creating Oracle, MSSQL and PosgresSQL connectors</li>
                            <li>Incrementing column name to use to detect new rows is typically the ID column (Number) </li>
                            <li>Timestamp column name to detect new or modified rows is typically the Date Column (DATE2)</li>
<<<<<<< HEAD
                            <li>Incrementing and Timestamp column should be not null </li>
                            <li>Configuration Name should be unique</li>
=======
                            <li>Configuration Name should be unique and without spaces</li>
                            <li>When using Docker, User Containername as Host address in JDBC URL if Database deployed in docker else use IP host address </li>
>>>>>>> isha
                            <li>Table name specification is <b>schemaname. tablename</b> for PostgresSQL, <b>tablename</b> for Oracle and MSSQL </li>
                            <li>Please see the example configuration for more clarification</li>
                        </ul>
                    </div>
                </Card.Body>
            </Card>
            <div className="dataconnectorform-container">

                <Form onSubmit={handleSubmit} className="dataconnectorform-form">

                    <Form.Group controlId="Connection User" className="form-group-custom">
                        <Form.Label>Connection User *</Form.Label>
                        <Form.Control className="form-control-custom" required type="text" placeholder='Enter the username for your database connection' value={connectionuser} onChange={(e) => setconnectionuser(e.target.value)} />
                    </Form.Group>
                    <Form.Group controlId="Connection Password" className="form-group-custom">
                        <Form.Label>Connection Password *</Form.Label>
                        <Form.Control className="form-control-custom" required type="text" placeholder='Enter the password for your database connection' value={connectionpassword} onChange={(e) => setconnectionpassword(e.target.value)} />
                    </Form.Group>
                    <Form.Group controlId="Name" className="form-group-custom">
                        <Form.Label>Name *</Form.Label>
                        <Form.Control className="form-control-custom" required type="text" placeholder='Enter the name for your connector' value={name} onChange={(e) => setname(e.target.value)} />
                    </Form.Group>
                    <Form.Group controlId="Mode" className="form-group-custom">
                        <Form.Label>Mode *</Form.Label>
                        <Form.Control as="select" value={mode} required placeholder='Select the mode for the connector (incrementing for id column, timestamp for date column)' onChange={(e) => setMode(e.target.value)}>
                            <option value="" disabled>Select mode for the connector</option>
                            <option value="incrementing">Incrementing</option>
                            <option value="timestamp">Timestamp</option>
                        </Form.Control>
                    </Form.Group>

                    {mode === 'incrementing' ? (
                        <Form.Group controlId="IncrementingColumnName" className="form-group-custom">
                            <Form.Label>Incrementing Column Name *</Form.Label>
                            <Form.Control className="form-control-custom" placeholder='Enter the incrementing column name' type="text" value={incrementingcolumnname} onChange={(e) => setincrementingcolumnname(e.target.value)} />
                        </Form.Group>
                    ) : (
                        <Form.Group controlId="TimestampColumnName" className="form-group-custom">
                            <Form.Label>Timestamp Column Name *</Form.Label>
                            <Form.Control className="form-control-custom" placeholder='Enter the timestamp column name' type="text" value={timestampColumnName} onChange={(e) => setTimestampColumnName(e.target.value)} />
                        </Form.Group>
                    )}
                    <Form.Group controlId="Key Converter Schemas Enable" className="form-group-custom">
                        <Form.Label>Key Converter Schemas Enable *</Form.Label>
                        <Form.Control className="form-control-custom" required type="text" placeholder='Enable schema for key converter? (true/false)' value={keyconverterschemasenable} onChange={(e) => setkeyconverterschemasenableKafkaTopic(e.target.value)} />
                    </Form.Group>
                    <Form.Group controlId="Topic Prefix" className="form-group-custom">
                        <Form.Label>Topic Prefix *</Form.Label>
                        <Form.Control className="form-control-custom" required placeholder='Enter the prefix name for the Kafka topic' type="text" value={topicprefix} onChange={(e) => settopicprefix(e.target.value)} />
                    </Form.Group>

                    <Form.Group controlId="Value Converter Schemas Enable" className="form-group-custom">
                        <Form.Label>Value Converter Schemas Enable *</Form.Label>
                        <Form.Control className="form-control-custom" required placeholder='Enable schema for value converter? (true/false)' type="text" value={valueconverterschemasenable} onChange={(e) => setvalueconverterschemasenable(e.target.value)} />
                    </Form.Group>

                    <Form.Group controlId="Connection URL" className="form-group-custom">
                        <Form.Label>Connection URL *</Form.Label>
                        <Form.Control className="form-control-custom" required placeholder='Enter the JDBC Connection URL for your database connection' type="text" value={connectionurl} onChange={(e) => setconnectionurl(e.target.value)} />
                    </Form.Group>
                    <Form.Group controlId="Table Include List" className="form-group-custom">
                        <Form.Label>Table Include List *</Form.Label>
                        <Form.Control className="form-control-custom" required placeholder='Enter the list of tables to include, separated by commas' type="text" value={tableincludelist} onChange={(e) => settableincludelist(e.target.value)} />
                    </Form.Group>
                    <Button variant="primary" type="submit">
                        Publish
                    </Button>
                </Form>

                <div className="dataconnectorform-textbox-container">
                    <Form.Group controlId="textbox" className="dataconnectorform-textbox-group">
                        <Form.Label>Example Configuration</Form.Label>
                        <Form.Control className="dataconnectorform-textbox form-control-custom" as="textarea" rows={3} defaultValue={jsonConfig}
                            readOnly />
                    </Form.Group>
                </div>
            </div>
        </Layoutnavbar>
    );
}

export default Dataconnectorform;
