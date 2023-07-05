import React, { useState } from 'react';
import { Container, Row, Col, Nav, Button, Navbar, Dropdown } from 'react-bootstrap';
import MenuIcon from '@mui/icons-material/Menu';
import { Link } from 'react-router-dom';
import "../styles/Layoutnavbar.css";

const Layoutnavbar = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="sm"  className="d-flex justify-content-between" >
      <div>
          <Button variant="link" onClick={() => setSidebarOpen(!sidebarOpen)}>
            <MenuIcon style={{ color: "white" }}/>
          </Button>
          <Navbar.Brand>KafkaSteelO</Navbar.Brand>
        </div>
        <div>
          <Dropdown className='me-3'>
            <Dropdown.Toggle className='dropdown-toggle-custom' id="dropdown-basic">
              Apache Kafka
            </Dropdown.Toggle>
            
            <Dropdown.Menu className='dropdown-menu-custom'>
              <Dropdown.Item className='custom-dropdown-item' href="http://localhost:3002/ui/clusters/local/all-topics">Kafka Topic</Dropdown.Item>
              <Dropdown.Item className='custom-dropdown-item' href="http://localhost:3002/ui/clusters/local/connectors">Kafka Connect</Dropdown.Item>
              {/* Add more items here as needed */}
            </Dropdown.Menu>
            
          </Dropdown>
          </div>
        {/* <Navbar.Toggle aria-controls="basic-navbar-nav" onClick={() => setSidebarOpen(!sidebarOpen)} /> */}
      </Navbar>
      <Container fluid>
        <Row>
          {sidebarOpen && (
            <Col sm={2} className="bg-primary sidebar">
              <Nav variant="pills" className=" flex-column">
                <Nav.Item>
                  <Nav.Link as={Link} to='/Filetypecsv' className="text-white" >CSV File</Nav.Link>
                  <Nav.Link as={Link} to='/Filetypeapi' className="text-white" >API</Nav.Link>
                  <Nav.Link as={Link} to='/Filetypeparquet' className="text-white">Parquet File</Nav.Link>
                  <Nav.Link as={Link} to='/Opcuadata' className="text-white">OPCUA Data</Nav.Link>
                  <Nav.Link as={Link} to='/Persistdataform' className="text-white">Persist Data</Nav.Link>
                  <Nav.Link as={Link} to='/Dataconnectorform' className="text-white"> RDBMS Connector</Nav.Link>
                </Nav.Item>
              </Nav>
            </Col>
          )}
          <Col sm={sidebarOpen ? 9 : 12}>
            {children}
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Layoutnavbar;
