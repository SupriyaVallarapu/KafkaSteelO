import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import Layout from '../Layouts/Layout';

function Filetypeparquet() {
  const [dataDir, setDataDir] = useState('');
  const [kafkaBroker, setKafkaBroker] = useState('');
  const [kafkaTopic, setKafkaTopic] = useState('');
  const [timecolumnname, settimecolumnname] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Create a JSON payload with the form data
    const payload = {
      data_dir: dataDir,
      kafka_broker: kafkaBroker,
      kafka_topic: kafkaTopic,
      time_column_name: timecolumnname
    };

    // Make a POST request to the backend API
    fetch('http://localhost:8080/api/parquetupload', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
      .then(response => {
        if (response.ok) {
          // Handle successful response
          console.log('Data uploaded successfully!');
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


    <Layout>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId='dataDir'>
          <Form.Label>Data Directory Path </Form.Label>
          < Form.Control type="text" value={dataDir} onChange={(e) => setDataDir(e.target.value)}></Form.Control>
        </Form.Group>
        <Form.Group controlId='kafkaBroker'>
          <Form.Label>Kafka Broker: </Form.Label>
          < Form.Control type="text" value={kafkaBroker} onChange={(e) => setKafkaBroker(e.target.value)}></Form.Control>
        </Form.Group>
        <Form.Group controlId='kafkaTopic'>
          <Form.Label>Kafka Topic: </Form.Label>
          < Form.Control type="text" value={kafkaTopic} onChange={(e) => setKafkaTopic(e.target.value)}></Form.Control>
        </Form.Group>
        <Form.Group controlId='timecolumnname'>
          <Form.Label>Time Column Name </Form.Label>
          < Form.Control type="text" value={timecolumnname} onChange={(e) => settimecolumnname(e.target.value)}></Form.Control>
        </Form.Group>
        <Button variant='primary' type="submit">Publish</Button>
      </Form>
    </Layout>
  );
}

export default Filetypeparquet;