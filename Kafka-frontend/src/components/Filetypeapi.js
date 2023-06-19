import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
//import { useNavigate } from "react-router-dom";
import Layoutnavbar from '../Layouts/Layoutnavbar';
import { SuccessfulUploadAlert, FailedUploadAlert, EmptyFieldAlert, URLAlert } from '../Alerts/Alerts.js';


let id = 0;
function Filetypeapi() {

  //const navigate=useNavigate();
  const [apiurl, setapiurl] = useState('');
  //https://jsonplaceholder.typicode.com/users
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
    setAlerts([]);

    if (!apiurl || !kafkaBroker || !kafkaTopic) {
      addAlert(<EmptyFieldAlert />);
      return;
    }

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
          return response.json();
        } else {
          if (response.status === 500) {
            // Create a custom alert for HTTP 500 errors
            addAlert(<URLAlert />);
            throw new Error('Internal Server Error');
          }
        }
      })
      .then(data => {
        // Handle successful response
        addAlert(<SuccessfulUploadAlert />);
      })
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
