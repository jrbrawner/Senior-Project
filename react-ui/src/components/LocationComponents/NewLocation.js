import React from 'react';
import UserDataService from '../../services/user.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';

export default function App() {
  
  const navigate = useNavigate(); 
  const params = useParams();
  
  const handleNewSubmit = e => {
    e.preventDefault();
    const formData = new FormData(e.target);
    //formData.append('userId', user.id);
    
    UserDataService.create(formData).then((response) =>
    {
      if (response.status === 201){
          navigate('/user');
      }
    }).catch(error => {
        if (error.response.status === 400){
          alert("Error");
        }});
  }

  return (
    <Form onSubmit={handleNewSubmit}>

      <Form.Group className="mb-3" controlId="formUserName">
        <Form.Label>Name</Form.Label>
        <Form.Control
            required
            type="text"
            name="name"
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserEmail">
        <Form.Label>Email</Form.Label>
        <Form.Control
            required
            type="text"
            name="email"
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control
            required
            type="text"
            name="password"
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserPhoneNumber">
        <Form.Label>Phone Number</Form.Label>
        <Form.Control
            required
            type="text"
            name="phoneNumber"
          />
      </Form.Group>


      <Form.Group className="mb-3" controlId="formUserLocation">
        <Form.Label>Location ID</Form.Label>
        <Form.Control
            required
            type="text"
            name="locationId"/>
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserRole">
        <Form.Label>Role</Form.Label>
        <Form.Control
            required
            type="text"
            name="role"
          />
      </Form.Group>

      <Button variant="primary" type="submit">
        Create User
      </Button>
    </Form>
  )
  

}