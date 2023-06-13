import React, { useState } from 'react';
import './Filetypecsv.css';
import {  Form, Button } from 'react-bootstrap';

import Layout from '../Layouts/Layout';

function Filetypecsv() {
  const [dataDir, setDataDir] = useState('');
  const [kafkaBroker, setKafkaBroker] = useState('');
  const [kafkaTopic, setKafkaTopic] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = {
      data_dir: dataDir,
      kafka_broker: kafkaBroker,
      kafka_topic: kafkaTopic
    };
    console.log(payload);

    fetch('http://localhost:8080/api/csvupload', {
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
  };

  return (
    <Layout>

      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="directoryPath" className="form-group-custom">
          <Form.Label>Directory Path:</Form.Label>
          <Form.Control className="form-control-custom" type="text" value={dataDir} onChange={(e) => setDataDir(e.target.value)} />
        </Form.Group>
        <Form.Group controlId="kafkaBroker" className="form-group-custom">
          <Form.Label>Kafka Broker:</Form.Label>
          <Form.Control className="form-control-custom" type="text" value={kafkaBroker} onChange={(e) => setKafkaBroker(e.target.value)} />
        </Form.Group>
        <Form.Group controlId="kafkaTopic" className="form-group-custom">
          <Form.Label>Kafka Topic:</Form.Label>
          <Form.Control className="form-control-custom" type="text" value={kafkaTopic} onChange={(e) => setKafkaTopic(e.target.value)} />
        </Form.Group>
        <Button variant="primary" type="submit">
          Publish
        </Button>
      </Form>

    </Layout>
  );
}

export default Filetypecsv;

