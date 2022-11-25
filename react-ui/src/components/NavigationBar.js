import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import React from 'react';
import Cookies from 'js-cookie';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';

export default function NavigationBar(props){

    const state = {
      username: Cookies.get('name'),
      roles: Cookies.get('roles')
    }

    const search = ({ target: { value } }) => {
      console.log(value);
    };
    

  
  if (state.roles != undefined){
    if (state.roles.includes("Super Admin")){
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
                
              <Form className="d-flex" onSubmit={search} >
                <Form.Control
                  type="search"
                  placeholder="Search"
                  name="search"
                  className="me-2"
                  defaultValue=""
                  aria-label="Search"
                  />
                <Button variant="outline-success" type="submit" >Search</Button>
              </Form>
              <Nav>
                <Nav.Link href="/notifications">Notifications</Nav.Link>
              </Nav>
              
              <Nav>
                <Nav.Link href="/role">Role Management</Nav.Link>
              </Nav>
              
              <NavDropdown title={<img src="person-circle.svg"/>}>
                <NavDropdown.Item><i className="fa fa-envelope fa-fw"></i>Profile</NavDropdown.Item>
                <NavDropdown.Item><i className="fa fa-gear fa-fw"></i>Settings</NavDropdown.Item>
                <NavDropdown.Item divider />
                <NavDropdown.Item href="/logout" eventKey='3'><i className="fa fa-sign-out fa-fw"></i>Logout</NavDropdown.Item>
              </NavDropdown>
          </Container>
        </Navbar>
    );
    }
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
          <Nav>
            <Nav.Link href="/notifications">Notifications</Nav.Link>
          </Nav>
          
          <NavDropdown title={<img src="person-circle.svg"/>}>
              <NavDropdown.Item href="/profile" eventkey='1'><i className="fa fa-envelope fa-fw"></i>Profile</NavDropdown.Item>
              <NavDropdown.Item><i className="fa fa-gear fa-fw"></i>Settings</NavDropdown.Item>
              <NavDropdown.Item divider />
              <NavDropdown.Item href="/logout" eventKey='3'><i className="fa fa-sign-out fa-fw"></i>Logout</NavDropdown.Item>
          </NavDropdown>

      </Container>
    </Navbar>
  );
  
}

