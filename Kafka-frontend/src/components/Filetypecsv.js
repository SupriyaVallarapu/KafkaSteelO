import React, { useState } from 'react';
import '../styles/Filetypecsv.css';
import { Form, Button } from 'react-bootstrap';
import Layoutnavbar from '../Layouts/Layoutnavbar';
import { Card } from 'react-bootstrap';
import { SuccessfulUploadAlert, FailedUploadAlert, EmptyFieldAlert, DirectoryPathDoesntExistAlert, NoFilesInPathAlert } from '../Alerts/Alerts.js';
//import { HOST_PORT } from '../../ENV_VAR';

let id = 0;
function Filetypecsv() {
  const [dataDir, setDataDir] = useState('');
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
    if (!dataDir || !kafkaBroker || !kafkaTopic) {
      addAlert(<EmptyFieldAlert />);
      return;
    }

    const payload = {
      data_dir: dataDir,
      kafka_broker: kafkaBroker,
      kafka_topic: kafkaTopic
    };

    fetch('http://localhost:8080/api/csvupload', {
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
              case `Directory ${dataDir} does not exist`:
                addAlert(<DirectoryPathDoesntExistAlert />);
                break;
              case `No CSV files found in directory ${dataDir}`:
                addAlert(<NoFilesInPathAlert />);
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
            <li>Kafka Broker: example: localhost:9092 or when using docker - Kafka1: 19092 ( containername: docker internal port number )</li>
            <li>Directory path is the mapped folder path of docker container (/app/data) or local folder if not deployed</li>
            <li>Valid characters for Kafka topics are the ASCII Alphanumeric characters, ‘.’, ‘_’, and ‘-‘. No spaces allowed. <br></br>
              Period (‘.’) or underscore (‘_’) could collide. To avoid issues it is best to use either, but not both.</li>
            <li>Topic name should be a unique name </li>

          </ul>
        </Card.Body>
      </Card>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="directoryPath" className="form-group-custom">
          <Form.Label>Directory Path *</Form.Label>
          <Form.Control className="form-control-custom" required type="text" placeholder="Enter path for files" value={dataDir} onChange={(e) => setDataDir(e.target.value)} />
        </Form.Group>
        <Form.Group controlId="kafkaBroker" className="form-group-custom">
          <Form.Label>Kafka Broker *</Form.Label>
          <Form.Control className="form-control-custom" required type="text" placeholder="Enter Kafka Broker:" value={kafkaBroker} onChange={(e) => setKafkaBroker(e.target.value)} />
        </Form.Group>
        <Form.Group controlId="kafkaTopic" className="form-group-custom">
          <Form.Label>Kafka Topic Name *</Form.Label>
          <Form.Control className="form-control-custom" required type="text" placeholder='Enter Kafka Topic' value={kafkaTopic} onChange={(e) => setKafkaTopic(e.target.value)} />
        </Form.Group>
        <Button variant="primary" type="submit">
          Publish
        </Button>
      </Form>
    </Layoutnavbar>
  );
}

export default Filetypecsv;
