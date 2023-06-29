import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import Layoutnavbar from '../Layouts/Layoutnavbar';
//import { useNavigate } from 'react-router-dom';
import { SuccessfulUploadAlert, FailedUploadAlert, EmptyFieldAlert, DirectoryPathDoesntExistAlert, NoFilesInPathAlert } from '../Alerts/Alerts.js';

let id = 0;
function Filetypeparquet() {
  const [dataDir, setDataDir] = useState('');
  const [kafkaBroker, setKafkaBroker] = useState('');
  const [kafkaTopic, setKafkaTopic] = useState('');
  const [timecolumnname, settimecolumnname] = useState('');
  const [alerts, setAlerts] = useState([]);

  //const [showPersistDialog, setShowPersistDialog] = useState(false);
  //let navigate=useNavigate();
  const addAlert = (component) => {
    setAlerts(alerts => [...alerts, { id: id++, component }]);
  };

  const removeAlert = (id) => {
    setAlerts(alerts => alerts.filter(alert => alert.id !== id));
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    setAlerts([]);

    // Create a JSON payload with the form data
    if (!dataDir || !kafkaBroker || !kafkaTopic || !timecolumnname) {
      addAlert(<EmptyFieldAlert />);
      return;
    }
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
          return response.json();
        } else {
          throw response;
        }
      })
      .then(data => {
        addAlert(<SuccessfulUploadAlert />);
      })
      .catch(errorResponse => {
        // Check if errorResponse has a 'Content-Type' of 'application/json'
        if (errorResponse.headers.get('Content-Type') === 'application/json') {
          errorResponse.json().then(error => {
            switch (error.error) {
              case `Directory ${dataDir} does not exist`:
                addAlert(<DirectoryPathDoesntExistAlert />);
                break;
              case `No Parquet files found in directory ${dataDir}`:
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
      <h3>Instructions</h3>
      <br></br>
      <ul>
        <li>All fields marked * are mandatory</li>
        <li>Valid characters for Kafka topics are the ASCII Alphanumeric characters, ‘.’, ‘_’, and ‘-‘. No spaces allowed. <br></br>
          Period (‘.’) or underscore (‘_’) could collide. To avoid issues it is best to use either, but not both.</li>
      </ul>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId='dataDir'>
          <Form.Label>Data Directory Path *</Form.Label>
          < Form.Control type="text" required value={dataDir} placeholder="Enter directory folder path of Parquet files" onChange={(e) => setDataDir(e.target.value)}></Form.Control>
        </Form.Group>
        <Form.Group controlId='kafkaBroker'>
          <Form.Label>Kafka Broker *</Form.Label>
          < Form.Control type="text" required value={kafkaBroker} placeholder="Enter Kafka Broker: example: localhost:9092" onChange={(e) => setKafkaBroker(e.target.value)}></Form.Control>
        </Form.Group>
        <Form.Group controlId='kafkaTopic'>
          <Form.Label>Kafka Topic Name *</Form.Label>
          < Form.Control type="text" required value={kafkaTopic} placeholder='Enter Kafka Topic' onChange={(e) => setKafkaTopic(e.target.value)}></Form.Control>
        </Form.Group>
        <Form.Group controlId='timecolumnname'>
          <Form.Label>Time Column Name *</Form.Label>
          < Form.Control type="text" required value={timecolumnname} placeholder='Enter time column name' onChange={(e) => settimecolumnname(e.target.value)}></Form.Control>
        </Form.Group>
        <Button variant='primary' type="submit">Publish</Button>
      </Form>
    </Layoutnavbar>
  );
}

export default Filetypeparquet;