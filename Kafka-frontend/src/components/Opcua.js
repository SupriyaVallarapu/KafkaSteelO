import React, { useState } from 'react';
import './Filetypecsv.css';
import { Form, Button } from 'react-bootstrap';
import Layoutnavbar from '../Layouts/Layoutnavbar';
import { SuccessfulUploadAlert, FailedUploadAlert, EmptyFieldAlert, OpcuaURLconnectAlert } from '../Alerts/Alerts.js';

let id = 0;
function Opcua() {
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
            node_ids:nodeids
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
                            case 'could not connect to ${opcua}':
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

            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="opcuaurl" className="form-group-custom">
                    <Form.Label>OPCUA URL:</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={opcuaurl} onChange={(e) => setopcuaurl(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="kafkaBroker" className="form-group-custom">
                    <Form.Label>Kafka Broker:</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={kafkaBroker} onChange={(e) => setKafkaBroker(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="kafkaTopic" className="form-group-custom">
                    <Form.Label>Kafka Topic:</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={kafkaTopic} onChange={(e) => setKafkaTopic(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="nodeids" className="form-group-custom">
                    <Form.Label>Node IDs:</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={nodeids} onChange={(e) => setnodeids(e.target.value)} />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Publish
                </Button>
            </Form>
        </Layoutnavbar>
    );
}

export default Opcua;
