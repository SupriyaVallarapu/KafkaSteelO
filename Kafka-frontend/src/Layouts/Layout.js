import React, { useState } from 'react';
import { Container, Row, Col, Nav, Form, Button, Navbar, NavbarBrand } from 'react-bootstrap';
import MenuIcon from '@mui/icons-material/Menu';
import { Link } from 'react-router-dom';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="sm">
        <Button variant="link" onClick={() => setSidebarOpen(!sidebarOpen)}>
            <MenuIcon style={{ color: "white" }}/>
        </Button>
        <Navbar.Brand> KakfaSteelO </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" onClick={() => setSidebarOpen(!sidebarOpen)} />
      </Navbar>
      <Container fluid>
        <Row>
          {sidebarOpen && (
            <Col sm={2} className="bg-primary sidebar">
              <Nav variant="pills" className=" flex-column">
                <Nav.Item>
                  <Nav.Link as={Link} to='/' className="text-white" >CSV File</Nav.Link>
                  <Nav.Link as={Link} to='/Filetypeapi' className="text-white" >Api File</Nav.Link>
                  <Nav.Link as={Link} to='/Filetypeparquet' className="text-white">Parquet File</Nav.Link>
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

export default Layout;
