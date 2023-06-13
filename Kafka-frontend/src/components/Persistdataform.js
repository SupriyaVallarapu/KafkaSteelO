import React, { useState } from 'react';
import Layoutnavbar from '../Layouts/Layoutnavbar';
import { Modal, Form, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
function Persistdataform() {

    const location = useLocation();
    const { dataDir, kafkaBroker, kafkaTopic } = location.state || {};
    const [dbname, setdbname] = useState('');
    const [dbschema, setdbschema] = useState('');
    const [dbuser, setdbuser] = useState('')
    const [dbpassword, setdbpassword] = useState('');
    const [dbhost, setdbhost] = useState('')
    const [dbport, setdbport] = useState('')
    const [offset,setoffset]=useState('')
    const [consumergroup,setconsumergroup]=useState('')
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();

        const payload = {
            data_dir: dataDir,
            kafka_broker: kafkaBroker,
            kafka_topic: kafkaTopic,
            db_name: dbname,
            db_schema:dbschema,
            db_user: dbuser,
            db_password:dbpassword,
            db_host: dbhost,
            db_port:dbport,
            offset:offset,
            consumer_group:consumergroup

          };
          console.log(payload);
      
          fetch('http://localhost:8080/api/consume_kafka', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
          })
            .then(response => {
              if (response.ok) {
                console.log(payload);
                console.log('Data uploaded successfully!');
              } else {
                console.log('Failed to upload data.');
              }
            })
            .catch(error => {
              console.error('Error:', error);
            });

        // You can handle the form submission here
        console.log('Form submitted with the following values:');
        console.log(`Directory Path: ${dataDir}`);
        console.log(`Kafka Broker: ${kafkaBroker}`);
        console.log(`Kafka Topic: ${kafkaTopic}`);
        console.log(`DB Name: ${dbname}`);
        console.log(`DB Password: ${dbpassword}`);
        navigate('/Filetypecsv');
    };
    return (
<Layoutnavbar>

        <Form onSubmit={handleSubmit}>
            <h4>Persist Data</h4>
            <Form.Group controlId="directoryPath">
                <Form.Label>Directory Path:</Form.Label>
                <Form.Control type="text" value={dataDir} readOnly />
            </Form.Group>
            <Form.Group controlId="kafkaBroker">
                <Form.Label>Kafka Broker:</Form.Label>
                <Form.Control type="text" value={kafkaBroker} readOnly />
            </Form.Group>
            <Form.Group controlId="kafkaTopic">
                <Form.Label>Kafka Topic:</Form.Label>
                <Form.Control type="text" value={kafkaTopic} readOnly />
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
            <Button variant="primary" type="submit">
                Publish
            </Button>
        </Form>


        </Layoutnavbar>

    );
}


export default Persistdataform;