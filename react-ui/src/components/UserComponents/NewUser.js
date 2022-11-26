import React from 'react';
import MessageDataService from '../../services/message.service';
import UserDataService from '../../services/user.service';
import RoleDataService from '../../services/role.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';

export default function App() {
  
  const navigate = useNavigate(); 
  const params = useParams();
  const [locations, setLocations] = React.useState();
  const [roles, setRoles] = React.useState();

  React.useEffect(() => {
    UserDataService.getAvailableLocations().then((response) => {
      setLocations(response.data);
    });

    RoleDataService.getAvailableRoles().then((response) => {
      setRoles(response.data);
    } )

  }, []);
  
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
          alert(error.response.data["msg"]);
        }});
  }

  if (!locations)  return (<Spinner animation="border" role="status">
  <span className="visually-hidden">Loading...</span>
</Spinner>)

if (!roles)  return (<Spinner animation="border" role="status">
  <span className="visually-hidden">Loading...</span>
</Spinner>)

  return (
    <Form onSubmit={handleNewSubmit}>

      <Form.Group className="mb-3" controlId="formUserName">
        <Form.Label>Name</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="name"
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserEmail">
        <Form.Label>Email</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="email"
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="password"
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserPhoneNumber">
        <Form.Label>Phone Number</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="phoneNumber"
          />
      </Form.Group>

      <div className="mb-3">
      <h4>Select Users Locations</h4>
      {locations.map((location) => {
            return (
                <div>
                <Form.Check
                    type={"checkbox"}
                    defaultChecked={false}
                    id={`${location.name}`}
                    name={`${location.name}`}
                    label={`${location.name}`}
                    />
                </div>
            )
      })}
      </div>

      <h4>Select Users Role</h4>
      {roles.map((role) => {
            return (
                <div>
                <Form.Check 
                    type={"radio"}
                    defaultChecked={false}
                    id={`${role.name}`}
                    name="roleGroup"
                    value={`${role.name}`}
                    label={`${role.name}`}
                    />
                </div>
            )
      })}

      <Button className="mt-2" variant="primary" type="submit">
        Create User
      </Button>
    </Form>
  )
  

}