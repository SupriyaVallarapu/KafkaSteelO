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


// import React, { useState } from 'react';

// function Filetypecsv() {
//   const [dataDir, setDataDir] = useState('');
//   const [kafkaBroker, setKafkaBroker] = useState('');
//   const [kafkaTopic, setKafkaTopic] = useState('');
//   const [fileType, setFileType] = useState('csv'); // Default to CSV

//   const handleSubmit = (e) => {
//     e.preventDefault();

//     // Create a JSON payload with the form data
//     const payload = {
//       data_dir: dataDir,
//       kafka_broker: kafkaBroker,
//       kafka_topic: kafkaTopic
//     };

//     // Determine the API endpoint based on the selected file type
//     const apiEndpoint = fileType === 'csv' ? 'http://localhost:8080/api/csvupload' : 'http://localhost:8080/api/logupload';

//     // Make a POST request to the backend API
//     fetch(apiEndpoint, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify(payload)
//     })
//       .then(response => {
//         if (response.ok) {
//           // Handle successful response
//           console.log('Data uploaded successfully!');
//         } else {
//           // Handle error response
//           console.log('Failed to upload data.');
//         }
//       })
//       .catch(error => {
//         console.error('Error:', error);
//       });
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <label>
//         Directory Path:
//         <input type="text" value={dataDir} onChange={(e) => setDataDir(e.target.value)} />
//       </label>
//       <br />
//       <label>
//         Kafka Broker:
//         <input type="text" value={kafkaBroker} onChange={(e) => setKafkaBroker(e.target.value)} />
//       </label>
//       <br />
//       <label>
//         Kafka Topic:
//         <input type="text" value={kafkaTopic} onChange={(e) => setKafkaTopic(e.target.value)} />
//       </label>
//       <br />
//       <label>
//         File Type:
//         <select value={fileType} onChange={(e) => setFileType(e.target.value)}>
//           <option value="csv">CSV</option>
//           <option value="log">Log</option>
//         </select>
//       </label>
//       <br />
//       <button type="submit">Upload</button>
//     </form>
//   );
// }

// export default Filetypecsv;
