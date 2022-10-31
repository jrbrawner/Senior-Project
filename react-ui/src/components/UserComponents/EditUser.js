import React from 'react';
import UserDataService from '../../services/user.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';

export default function App() {
  const [user, setUser] = React.useState(null);

  const navigate = useNavigate(); 
  const params = useParams();
  
  
  React.useEffect(() => {
    UserDataService.get(params.userId).then((response) => {
      setUser(response.data);
    });

  }, []);

  const handleEditSubmit = e => {
    e.preventDefault();
    const formData = new FormData(e.target);
    formData.append('userId', user.id);
    
    UserDataService.update(params.userId, formData).then((response) =>
    {
      if (response.status === 200){
          navigate('/user');
      }
      else{
        alert("Error");
      }
      
    })
  }

  function deleteUser(userId) {
    UserDataService.delete(userId).then((response) =>
    {
      if (response.status === 200){
          navigate('/user');
      }
      else{
        alert("Error");
      }
      
    })
  }

  if (!user) return <p>Loading...</p>;

  return (
    <Form onSubmit={handleEditSubmit}>

      <Form.Group className="mb-3" controlId="formUserName">
        <Form.Label>Name</Form.Label>
        <Form.Control
            required
            type="text"
            name="name"
            defaultValue={user.name}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserEmail">
        <Form.Label>Email</Form.Label>
        <Form.Control
            required
            type="text"
            name="email"
            defaultValue={user.email}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserLocation">
        <Form.Label>Location</Form.Label>
        <Form.Control
            required
            type="text"
            name="locationId"
            defaultValue={user.location_id}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserRoles">
        <Form.Label>Roles</Form.Label>
        <Form.Control
            required
            type="text"
            name="roles"
            defaultValue={user.roles.map((role) => (
                role.name))}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserPhoneNumber">
        <Form.Label>Phone Number</Form.Label>
        <Form.Control
            required
            type="text"
            name="phoneNumber"
            defaultValue={user.phone_number}
          />
      </Form.Group>

      <Button variant="primary" type="submit">
        Edit User
      </Button>
      <Button variant="danger" onClick={() => deleteUser(user.id)}>Delete User</Button>
    </Form>
  )
  

}