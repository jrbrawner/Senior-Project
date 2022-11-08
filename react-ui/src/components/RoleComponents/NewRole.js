import React from 'react';
import RoleDataService from '../../services/role.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';

export default function App() {

  
  const [permissions, setPermissions] = React.useState(0);

  const navigate = useNavigate(); 

  React.useEffect(() => {
    
    RoleDataService.getPermissions().then((response) => {
        setPermissions(response.data);
    })

  }, []);

  const handleSubmit = e => {
    e.preventDefault()
    const formData = new FormData(e.target);
    
    RoleDataService.create(formData).then((response) =>
    {
      if (response.status == 200){
          navigate('/role');
      }
      else{
        alert('Error');
      }
      
    })
  }

if (!permissions) return <Spinner animation="border" role="status">
<span className="visually-hidden">Loading...</span>
</Spinner>


  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="formRoleName">
        <Form.Label>Role Name</Form.Label>
        <Form.Control
            required
            type="text"
            name="name"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formRoleName">
        <Form.Label>Role Description</Form.Label>
        <Form.Control
            required
            type="text"
            name="description"
            defaultValue=""
          />
      </Form.Group>

      {permissions.map((permission) => {
        
            return (
                
                <div>
                <Form.Check 
                    type={"checkbox"}
                    id={`${permission}`}
                    defaultChecked={false}
                    name={permission.name}
                    label={`${permission.name}`}
                />
                <p>{permission.description}</p>
                </div>
            
      )})}

      <Button variant="primary" type="submit">
        Create New Role
      </Button>
    </Form>
  )
  

}