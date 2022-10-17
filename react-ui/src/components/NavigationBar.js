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
            <Nav.Link href="/user">People</Nav.Link>
            <NavDropdown title="Messages" id="navbarScrollingDropdown">

              <NavDropdown.Item href="/messages">Messages</NavDropdown.Item>
              <NavDropdown.Item href="#action5">
                Something else here
              </NavDropdown.Item>
            </NavDropdown>
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
          <Navbar.Text>
            Signed in as: <a href="/logout"> {state.username}
              </a>
          </Navbar.Text>
      </Container>
    </Navbar>
  );
}

