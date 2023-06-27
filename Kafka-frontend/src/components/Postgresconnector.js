import React, { useState } from 'react';
import './Filetypecsv.css';
import { Form, Button } from 'react-bootstrap';
import Layoutnavbar from '../Layouts/Layoutnavbar';
import { SuccessfulUploadAlert, FailedUploadAlert, EmptyFieldAlert } from '../Alerts/Alerts.js';

let id = 0;
function Postgresconnector() {
    const [incrementingcolumnname, setincrementingcolumnname] = useState('');
    const [timestampColumnName, setTimestampColumnName] = useState('');
    const [connectionpassword, setconnectionpassword] = useState('');
    const [keyconverterschemasenable, setkeyconverterschemasenableKafkaTopic] = useState('');
    const [topicprefix, settopicprefix] = useState('');
    const [connectionuser, setconnectionuser] = useState('');
    const [valueconverterschemasenable, setvalueconverterschemasenable] = useState('');
    const [name, setname] = useState('');
    const [mode, setMode] = useState('incrementing');
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
        if (!incrementingcolumnname || !connectionpassword ||
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

        fetch(`http://localhost:8080/api/postgresconnector`, {
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

            <Form onSubmit={handleSubmit}>

                <Form.Group controlId="Connection User" className="form-group-custom">
                    <Form.Label>Connection User</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={connectionuser} onChange={(e) => setconnectionuser(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="Connection Password" className="form-group-custom">
                    <Form.Label>Connection Password</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={connectionpassword} onChange={(e) => setconnectionpassword(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="Name" className="form-group-custom">
                    <Form.Label>Name</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={name} onChange={(e) => setname(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="Mode" className="form-group-custom">
                    <Form.Label>Mode</Form.Label>
                    <Form.Control as="select" value={mode} onChange={(e) => setMode(e.target.value)}>
                        <option value="incrementing">Incrementing</option>
                        <option value="timestamp">Timestamp</option>
                    </Form.Control>
                </Form.Group>

                {mode === 'incrementing' ? (
                    <Form.Group controlId="IncrementingColumnName" className="form-group-custom">
                        <Form.Label>Incrementing Column Name</Form.Label>
                        <Form.Control className="form-control-custom" type="text" value={incrementingcolumnname} onChange={(e) => setincrementingcolumnname(e.target.value)} />
                    </Form.Group>
                ) : (
                    <Form.Group controlId="TimestampColumnName" className="form-group-custom">
                        <Form.Label>Timestamp Column Name</Form.Label>
                        <Form.Control className="form-control-custom" type="text" value={timestampColumnName} onChange={(e) => setTimestampColumnName(e.target.value)} />
                    </Form.Group>
                )}
                

                <Form.Group controlId="Key Converter Schemas Enable" className="form-group-custom">
                    <Form.Label>Key Converter Schemas Enable</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={keyconverterschemasenable} onChange={(e) => setkeyconverterschemasenableKafkaTopic(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="Topic Prefix" className="form-group-custom">
                    <Form.Label>Topic Prefix</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={topicprefix} onChange={(e) => settopicprefix(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="Value Converter Schemas Enable" className="form-group-custom">
                    <Form.Label>Value Converter Schemas Enable</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={valueconverterschemasenable} onChange={(e) => setvalueconverterschemasenable(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="Connection URL" className="form-group-custom">
                    <Form.Label>Connection URL</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={connectionurl} onChange={(e) => setconnectionurl(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="Table Include List" className="form-group-custom">
                    <Form.Label>Table Include List</Form.Label>
                    <Form.Control className="form-control-custom" type="text" value={tableincludelist} onChange={(e) => settableincludelist(e.target.value)} />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Publish
                </Button>
            </Form>
        </Layoutnavbar>
    );
}

export default Postgresconnector;
