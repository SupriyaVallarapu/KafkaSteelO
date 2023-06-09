import React, { useState } from 'react';

function Filetypecsv() {
  const [dataDir, setDataDir] = useState('');
  const [kafkaBroker, setKafkaBroker] = useState('');
  const [kafkaTopic, setKafkaTopic] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Create a JSON payload with the form data
    const payload = {
      data_dir: dataDir,
      kafka_broker: kafkaBroker,
      kafka_topic: kafkaTopic
    };

    // Make a POST request to the backend API
    fetch('http://localhost:8080/api/csvupload', {
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
    <form onSubmit={handleSubmit}>
      <label>
        Directory Path:
        <input type="text" value={dataDir} onChange={(e) => setDataDir(e.target.value)} />
      </label>
      <br />
      <label>
        Kafka Broker:
        <input type="text" value={kafkaBroker} onChange={(e) => setKafkaBroker(e.target.value)} />
      </label>
      <br />
      <label>
        Kafka Topic:
        <input type="text" value={kafkaTopic} onChange={(e) => setKafkaTopic(e.target.value)} />
      </label>
      <br />
      <button type="submit">Upload</button>
    </form>
  );
}

export default Filetypecsv;
