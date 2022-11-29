import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import React from 'react';
import Cookies from 'js-cookie';
import logo from '../images/person-circle.svg';


export default function NavigationBar(props){
    const state = {
      username: Cookies.get('name'),
      roles: Cookies.get('roles')
    }

    const search = ({ target: { value } }) => {
      console.log(value);
    };
    

  
  if (state.roles != undefined){
    if (state.roles.includes("Super Admin") || state.roles.includes("Admin")){
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
                
              <Nav>
                <Nav.Link href="/role">Role Management</Nav.Link>
              </Nav>
              
              <NavDropdown drop={"start"} title={<img src={logo}/>}>
              <NavDropdown.Item href="/profile" eventKey='3'><i className="fa fa-sign-out fa-fw"></i>Profile</NavDropdown.Item>
                <NavDropdown.Item><i className="fa fa-gear fa-fw"></i>Settings</NavDropdown.Item>
                <NavDropdown.Item divider />
                <NavDropdown.Item href="/logout" eventKey='3'><i className="fa fa-sign-out fa-fw"></i>Logout</NavDropdown.Item>
              </NavDropdown>
          </Container>
        </Navbar>
    );
    }
  }
  if (state.roles != undefined){
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
          <NavDropdown drop={"start"} title={<img src={logo}/>}>
              <NavDropdown.Item href="/profile" eventKey='3'><i className="fa fa-sign-out fa-fw"></i>Profile</NavDropdown.Item>
              <NavDropdown.Item><i className="fa fa-gear fa-fw"></i>Settings</NavDropdown.Item>
              <NavDropdown.Item divider />
              <NavDropdown.Item href="/logout" eventKey='3'><i className="fa fa-sign-out fa-fw"></i>Logout</NavDropdown.Item>
          </NavDropdown>

      </Container>
    </Navbar>
  );
  }
}

