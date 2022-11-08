import React from 'react';
import UserDataService from '../../services/user.service';
import RoleDataService from '../../services/role.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';

export default function App() {
  const [user, setUser] = React.useState(null);
  const [roles, setRoles] = React.useState(null);

  const navigate = useNavigate(); 
  const params = useParams();
  
  
  React.useEffect(() => {
    UserDataService.get(params.userId).then((response) => {
      setUser(response.data);
    });
    RoleDataService.getAll().then((response) => {
        setRoles(response.data);
    })
  }, []);

  const handleEditSubmit = e => {
    e.preventDefault();
    const formData = new FormData(e.target);

    UserDataService.updateRoles(params.userId, formData).then((response) =>
    {
      if (response.status === 200){
          navigate('/role');
      }
      else{
        alert("Error");
      }
      
    })
  }

  

  

  if (!user) return <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>
  if (!roles) return <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>

  return (
    <Form onSubmit={handleEditSubmit}>

      <Form.Group className="mb-3" controlId="formUserName">
        <Form.Label>Name</Form.Label>
        <Form.Control
            disabled
            type="text"
            name="name"
            defaultValue={user.name}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserEmail">
        <Form.Label>Email</Form.Label>
        <Form.Control
            disabled
            type="text"
            name="email"
            defaultValue={user.email}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formUserLocation">
        <Form.Label>Location</Form.Label>
        <Form.Control
            disabled
            type="text"
            name="locationId"
            defaultValue={user.location_id}
          />
      </Form.Group>

      {roles.map((role) => {
        if (user.roles.some((x) => x.name === role.name)){
            return (
                <div>
                <Form.Check 
                    type={"checkbox"}
                    defaultChecked={true}
                    id={`${role.name}`}
                    name={role.name}
                    label={`${role.name}`}
                    />
                </div>
            )
        }
        else {
            return (
                <div>
                <Form.Check 
                    type={"checkbox"}
                    defaultChecked={false}
                    id={`${role.name}`}
                    name={role.name}
                    label={`${role.name}`}
                    />
                </div>
            )
        }
      })}

      
      <Button variant="primary" type="submit">
        Edit User
      </Button>
    </Form>
  )
  

}