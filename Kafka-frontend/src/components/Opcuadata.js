import React, { useState } from 'react';
import '../styles/Filetypecsv.css';
import { Form, Button } from 'react-bootstrap';
import Layoutnavbar from '../Layouts/Layoutnavbar';
import { SuccessfulUploadAlert, FailedUploadAlert, EmptyFieldAlert, OpcuaURLconnectAlert } from '../Alerts/Alerts.js';
import { Card } from 'react-bootstrap';
let id = 0;
function Opcuadata() {
    const [opcuaurl, setopcuaurl] = useState('');
    const [nodeids, setnodeids] = useState('');
    const [kafkaBroker, setKafkaBroker] = useState('');
    const [kafkaTopic, setKafkaTopic] = useState('');
    const [alerts, setAlerts] = useState([]);


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
        if (!opcuaurl || !kafkaBroker || !kafkaTopic || !nodeids) {
            addAlert(<EmptyFieldAlert />);
            return;
        }

        const payload = {
            opcua_url: opcuaurl,
            kafka_broker: kafkaBroker,
            kafka_topic: kafkaTopic,
            node_ids: nodeids
        };

        fetch('http://localhost:8080/api/opcuaproduce', {
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
            .catch(errorResponse => {
                // check if errorResponse has json method
                if (errorResponse.json) {
                    errorResponse.json().then(error => {
                        switch (error.error) {
                            case `could not connect to ${opcuaurl}`:
                                addAlert(<OpcuaURLconnectAlert />);
                                break;
                            default:
                                addAlert(<FailedUploadAlert />);
                                break;
                        }
                    });
                } else {
                    // In case of a network failure or other kind of request failure
                    console.error('An error occurred:', errorResponse);
                    addAlert(<FailedUploadAlert />);
                }
            });
    };

    return (
        <Layoutnavbar>
            {alerts.map(({ id, component }) => React.cloneElement(component, { key: id, onClose: () => removeAlert(id) }))}
            <Card className='instructions-container'>
        <Card.Body>
            <h3>Instructions</h3>
            <br></br>
            <ul>
                <li>All fields marked * are mandatory</li>
                <li>OPC URL format must be opc.tcp://localhost:4840 </li>
                <li>Valid characters for Kafka topics are the ASCII Alphanumeric characters, ‘.’, ‘_’, and ‘-‘. No spaces allowed. <br></br>
                    Period (‘.’) or underscore (‘_’) could collide. To avoid issues it is best to use either, but not both.</li>
                <li>Topic name should be a unique name </li>
                <li>Node IDs must be separated by commas (example - ns=2;i=4,ns=2;i=3):</li>
            </ul>
            </Card.Body>
            </Card>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="opcuaurl" className="form-group-custom">
                    <Form.Label>OPCUA URL *</Form.Label>
                    <Form.Control className="form-control-custom" required type="text" placeholder='Enter the URL of the OPCUA server' value={opcuaurl} onChange={(e) => setopcuaurl(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="kafkaBroker" className="form-group-custom">
                    <Form.Label>Kafka Broker *</Form.Label>
                    <Form.Control className="form-control-custom" required type="text" placeholder="Enter Kafka Broker: example: localhost:9092" value={kafkaBroker} onChange={(e) => setKafkaBroker(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="kafkaTopic" className="form-group-custom">
                    <Form.Label>Kafka Topic Name *</Form.Label>
                    <Form.Control className="form-control-custom" required type="text" placeholder='Enter Kafka Topic name' value={kafkaTopic} onChange={(e) => setKafkaTopic(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="nodeids" className="form-group-custom">
                    <Form.Label>Node IDs *</Form.Label>
                    <Form.Control className="form-control-custom" required type="text" placeholder='Enter the node IDs' value={nodeids} onChange={(e) => setnodeids(e.target.value)} />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Publish
                </Button>
            </Form>
        </Layoutnavbar>
    );
}

export default Opcuadata;
