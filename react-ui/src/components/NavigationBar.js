import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import React from 'react';
import Cookies from 'js-cookie';

export default function NavigationBar(){

    const state = {
      username: Cookies.get('name')
    }
    

  return (
    <Navbar bg="light" expand="sm">
      <Container>
        <Nav classname="me-auto">

            <Nav.Link href="/organization">Organizations</Nav.Link>
            <Nav.Link href="/location">Locations</Nav.Link>

            <NavDropdown title="People">
              <NavDropdown.Item href="/user">People</NavDropdown.Item> 
              <NavDropdown.Item href="/user/new">Pending Users</NavDropdown.Item>
            </NavDropdown>

            <Nav.Link href="/messages">Messages</Nav.Link>
            
        </Nav>
            
          <Form className="d-flex">
            <Form.Control
              type="search"
              placeholder="Search"
              className="me-2"
              aria-label="Search"
              />
            <Button variant="outline-success">Search</Button>
          </Form>
          <Nav className="">
            <Nav.Link>Notifications</Nav.Link>
          </Nav>
          <Navbar.Text>
            <a href="/logout"> {state.username}
              </a>
          </Navbar.Text>
      </Container>
    </Navbar>
  );
}

