import React, { useState ,useRef} from 'react';
import Layoutnavbar from '../Layouts/Layoutnavbar';
import { Form, Button } from 'react-bootstrap';
//import { useNavigate } from 'react-router-dom';
//import { useLocation } from 'react-router-dom';
import {
    SuccessfulUploadAlert,
    FailedUploadAlert,
    EmptyFieldAlert,
    RequestBodyErrorAlert,
    DBConnectionErrorAlert,
    CreateTableErrorAlert,
    TopicNotFoundErrorAlert,
    UnexpectedErrorAlert
} from '../Alerts/Alerts.js';

let id = 0;
function Persistdataform() {

    //const location = useLocation();
    //const { sourceType, dataDir, kafkaBroker, kafkaTopic, apiurl, timecolumnname} = location.state || {};
    const [kafkaBroker, setKafkaBroker] = useState('');
    const [kafkaTopic, setKafkaTopic] = useState('');
    const [dbname, setdbname] = useState('');
    const [dbschema, setdbschema] = useState('');
    const [dbuser, setdbuser] = useState('')
    const [dbpassword, setdbpassword] = useState('');
    const [dbhost, setdbhost] = useState('')
    const [dbport, setdbport] = useState('')
    const [offset, setoffset] = useState('')
    const [consumergroup, setconsumergroup] = useState('')
    const [data, setData] = useState('');
    const [alerts, setAlerts] = useState([]);
    const endpointRef = useRef(0);
    // const navigate = useNavigate();
    const addAlert = (component) => {
        setAlerts(alerts => [...alerts, { id: id++, component }]);
    };

    const removeAlert = (id) => {
        setAlerts(alerts => alerts.filter(alert => alert.id !== id));
    };
    const handleSubmit = (e) => {
        e.preventDefault();

        setAlerts([]);  // Clear previous alerts

        if (!kafkaBroker || !kafkaTopic || !dbname || !dbschema || !dbuser || !dbpassword || !dbhost || !dbport || !offset || !consumergroup) {
            addAlert(<EmptyFieldAlert />);
            return;
        }

        

        const payload = {
            kafka_broker: kafkaBroker,
            kafka_topic: kafkaTopic,
            db_name: dbname,
            db_schema: dbschema,
            db_user: dbuser,
            db_password: dbpassword,
            db_host: dbhost,
            db_port: dbport,
            offset: offset,
            consumer_group: consumergroup
        };
        const apiEndpoint = endpointRef.current === 0 ? 
            `http://localhost:8080/api/consume_and_persist_opcua` : 
            `http://localhost:8080/api/consume_and_persist`;

        // After using an endpoint, switch to the other one
        endpointRef.current = endpointRef.current === 0 ? 1 : 0;

        fetch(apiEndpoint, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response.ok) {
                    addAlert(<SuccessfulUploadAlert />);
                } else {
                    console.log(response);
                    throw response;
                    

                }
            })
            .catch(errorResponse => {
                if (errorResponse.json) {
                    
                    errorResponse.json().then(error => {
                        if (error.error.startsWith('Error parsing request body')) {
                            addAlert(<RequestBodyErrorAlert />);
                        } else if (error.error.startsWith('Error connecting to database')) {
                            addAlert(<DBConnectionErrorAlert />);
                        } else if (error.error.startsWith('Error creating table')) {
                            addAlert(<CreateTableErrorAlert />);
                        }
                        else if (error.error === "Kafka topic doesn't exist") {
                            addAlert(<TopicNotFoundErrorAlert />);
                        } else {
                            addAlert(<UnexpectedErrorAlert />);
                        }

                    });
                } else {
                    console.error('An error occurred:', errorResponse);
                    addAlert(<FailedUploadAlert />);
                }
            });

        //navigate('/Filetypecsv');



        // You can handle the form submission here
        console.log('Form submitted with the following values:');
        // console.log(`Directory Path: ${dataDir}`);
        console.log(`Kafka Broker: ${kafkaBroker}`);
        console.log(`Kafka Topic: ${kafkaTopic}`);
        console.log(`DB Name: ${dbname}`);
        console.log(`DB Password: ${dbpassword}`);
        //navigate('/Filetypecsv');
    };
    return (
        <Layoutnavbar>

            {alerts.map(({ id, component }) => React.cloneElement(component, { key: id, onClose: () => removeAlert(id) }))}
            <Form onSubmit={handleSubmit}>
                <h4>Persist Data</h4>

                {/* {sourceType === 'csv' && (
                    <Form.Group controlId="directoryPath">
                        <Form.Label>Directory Path:</Form.Label>
                        <Form.Control type="text" value={dataDir} readOnly />
                    </Form.Group>
                )}

                {sourceType === 'api' && (
                    <Form.Group controlId="apiurl">
                        <Form.Label>Api URL:</Form.Label>
                        <Form.Control type="text" value={apiurl} readOnly />
                    </Form.Group>
                )}
                {sourceType === 'parquet' && (
                    <Form.Group>
                        <Form.Group controlId="directoryPath">
                            <Form.Label>Directory Path:</Form.Label>
                            <Form.Control type="text" value={dataDir} readOnly />
                        </Form.Group>
                        <Form.Group controlId='timecolumnname'>
                            <Form.Label>Time Column Name </Form.Label>
                            < Form.Control type="text" value={timecolumnname} readOnly></Form.Control>
                        </Form.Group>
                    </Form.Group>
                )} */}
                <Form.Group controlId="kafkaBroker">
                    <Form.Label>Kafka Broker:</Form.Label>
                    <Form.Control type="text" value={kafkaBroker} onChange={(e) => setKafkaBroker(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="kafkaTopic">
                    <Form.Label>Kafka Topic:</Form.Label>
                    <Form.Control type="text" value={kafkaTopic} onChange={(e) => setKafkaTopic(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="dbname">
                    <Form.Label>DB Name:</Form.Label>
                    <Form.Control type="text" value={dbname} onChange={(e) => setdbname(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="dbschema">
                    <Form.Label>DB Schema:</Form.Label>
                    <Form.Control type="text" value={dbschema} onChange={(e) => setdbschema(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="dbuser">
                    <Form.Label>DB User:</Form.Label>
                    <Form.Control type="text" value={dbuser} onChange={(e) => setdbuser(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="dbPassword">
                    <Form.Label>DB Password:</Form.Label>
                    <Form.Control type="text" value={dbpassword} onChange={(e) => setdbpassword(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="dbhost">
                    <Form.Label>DB Host:</Form.Label>
                    <Form.Control type="text" value={dbhost} onChange={(e) => setdbhost(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="dbport">
                    <Form.Label>DB Port:</Form.Label>
                    <Form.Control type="number" value={dbport} onChange={(e) => setdbport(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="offset">
                    <Form.Label>Offset:</Form.Label>
                    <Form.Control type="text" value={offset} onChange={(e) => setoffset(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="consumergroup">
                    <Form.Label>Consumer Group</Form.Label>
                    <Form.Control type="text" value={consumergroup} onChange={(e) => setconsumergroup(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="dataType">
                    <Form.Label>Choose which data to Persist?:</Form.Label>
                    <Form.Control as="select" value={data} onChange={(e) => setData(e.target.value)}>
                        <option value="">Select</option>
                        <option value="opcua">Persist OPCUA Data</option>
                        <option value="normal">Persist CSV/API/Parquet Data</option>
                    </Form.Control>
                </Form.Group>
                <Button variant="primary" type="submit">
                    Publish
                </Button>
            </Form>


        </Layoutnavbar>

    );
}


export default Persistdataform;