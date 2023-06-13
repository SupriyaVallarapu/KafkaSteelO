import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

import Layoutnavbar from '../Layouts/Layoutnavbar';

function Filetypeapi() {
  const [apiurl, setapiurl] = useState('');
  //https://jsonplaceholder.typicode.com/users
  const [kafkaBroker, setKafkaBroker] = useState('');
  const [kafkaTopic, setKafkaTopic] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Create a JSON payload with the form data
    const payload = {
      api_url: apiurl,
      kafka_broker: kafkaBroker,
      kafka_topic: kafkaTopic
    };

    // Make a POST request to the backend API
    fetch('http://localhost:8080/api/apidata', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
      .then(response => {
        if (response.ok) {
          // Handle successful response
          console.log('Api Data uploaded successfully!');
        } else {
          // Handle error response
          console.log('Failed to upload data.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };



  return (
    <Layoutnavbar>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="apiurl">
          <Form.Label>Api URL:</Form.Label>
          <Form.Control type="text" value={apiurl} onChange={(e) => setapiurl(e.target.value)} />
        </Form.Group>

        <Form.Group controlId="kafkaBroker">
          <Form.Label>Kafka Broker:</Form.Label>
          <Form.Control type="text" value={kafkaBroker} onChange={(e) => setKafkaBroker(e.target.value)} />
        </Form.Group>
        <Form.Group controlId="kafkaTopic">
          <Form.Label>Kafka Topic:</Form.Label>
          <Form.Control type="text" value={kafkaTopic} onChange={(e) => setKafkaTopic(e.target.value)} />
        </Form.Group>
        <Button variant="primary" type="submit">
          Publish
        </Button>
      </Form>
    </Layoutnavbar>
  );
}

export default Filetypeapi;
