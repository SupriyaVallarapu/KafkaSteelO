import React, { useState } from 'react';
import './Filetypecsv.css';
import { Container, Row, Col, Nav, Form, Button, Navbar, NavbarBrand } from 'react-bootstrap';
import MenuIcon from '@mui/icons-material/Menu';

function Filetypecsv() {
  const [dataDir, setDataDir] = useState('');
  const [kafkaBroker, setKafkaBroker] = useState('');
  const [kafkaTopic, setKafkaTopic] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(true);

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
    <>
      <Navbar bg="dark" variant="dark" expand="sm">
      <Button variant="link" onClick={() => setSidebarOpen(!sidebarOpen)}>
          <MenuIcon style={{ color: "white" }}/>
        </Button>
        <Navbar.Brand href="#home" > KakfaSteelO
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" onClick={() => setSidebarOpen(!sidebarOpen)} />
      </Navbar>
      <Container fluid>
        <Row>
          {sidebarOpen && (
            <Col sm={2} className="bg-primary sidebar">
              <Nav variant="pills" className=" flex-column">
                <Nav.Item>
                  <Nav.Link className="text-white" >CSV File</Nav.Link>
                  <Nav.Link className="text-white" to='/Filetypelog'>Log File</Nav.Link>
                  <Nav.Link className="text-white">Parquet File</Nav.Link>
                </Nav.Item>
              </Nav>
            </Col>
          )}
          <Col sm={sidebarOpen ? 9 : 12}>
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
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default Filetypecsv;

