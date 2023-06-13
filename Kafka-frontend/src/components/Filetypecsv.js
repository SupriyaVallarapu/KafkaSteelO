import React, { useState } from 'react';
import './Filetypecsv.css';
import { Form, Button, Modal } from 'react-bootstrap';
import Layoutnavbar from '../Layouts/Layoutnavbar';
import { useNavigate } from "react-router-dom";

function Filetypecsv() {
  const [dataDir, setDataDir] = useState('');
  const [kafkaBroker, setKafkaBroker] = useState('');
  const [kafkaTopic, setKafkaTopic] = useState('');
  const [showPersistDialog, setShowPersistDialog] = useState(false);
  // const [showSecondForm, setShowSecondForm] = useState(false);
  const navigate=useNavigate();
  const handleSubmit = (e) => {
    e.preventDefault();
    setShowPersistDialog(true);

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

 

  const handlePersistData = (persist) => {
    setShowPersistDialog(false);
    if (persist) {
      navigate('/Persistdataform', { state:{ dataDir, kafkaBroker, kafkaTopic} });
    }
  }

  return (
    <Layoutnavbar>

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

      <Modal show={showPersistDialog} onHide={() => handlePersistData(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Persist Data</Modal.Title>
        </Modal.Header>
        <Modal.Body>Do you want to persist data?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => handlePersistData(false)}>No</Button>
          <Button variant="primary" onClick={() => handlePersistData(true)}>Yes</Button>
        </Modal.Footer>
      </Modal>
    </Layoutnavbar>
  );
}

export default Filetypecsv;

