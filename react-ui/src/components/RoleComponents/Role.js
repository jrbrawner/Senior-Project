import React from 'react';
import RoleDataService from '../../services/role.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';

export default function App() {

  const [role, setRole] = React.useState(null);
  const [permissions, setPermissions] = React.useState(0);

  const params = useParams();
  const navigate = useNavigate(); 

  React.useEffect(() => {
    RoleDataService.get(params.roleId).then((response) => {
      setRole(response.data);
      
      
    });

    RoleDataService.getPermissions().then((response) => {
        setPermissions(response.data);
    })

  }, []);

  const handleSubmit = e => {
    e.preventDefault()
    const formData = new FormData(e.target);
    
    RoleDataService.update(params.roleId, formData).then((response) =>
    {
      if (response.status == 200){
          navigate('/role');
      }
      else{
        alert('Error');
      }
      
    })
  }

  function deleteRole(roleId) {
    RoleDataService.delete(roleId).then((response) =>
    {
      if (response.status === 200){
          navigate('/role');
      }
      else{
        alert("Error");
      }
      
    })
  }

  if (!role && !permissions) return <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>

if (!role) return <Spinner animation="border" role="status">
<span className="visually-hidden">Loading...</span>
</Spinner>

if (!permissions) return <Spinner animation="border" role="status">
<span className="visually-hidden">Loading...</span>
</Spinner>


  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="formLocationName">
        <Form.Label>Role Name</Form.Label>
        <Form.Control
            required
            autoComplete="off"
            type="text"
            name="name"
            defaultValue={role.name}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationAddress">
        <Form.Label>Role Description</Form.Label>
        <Form.Control
            required
            autoComplete="off"
            type="text"
            name="description"
            defaultValue={role.description}
          />
      </Form.Group>

      {permissions.map((permission) => {
        if (role.permissions.some((x) => x.name === permission.name)){
            return (
                <div>
                <Form.Check 
                    type={"checkbox"}
                    defaultChecked={true}
                    id={`${permission}`}
                    name={permission.name}
                    label={`${permission.name}`}
                    />
                    <p>{permission.description}</p>
                </div>
            )
        }
        else {
            return (
                <div>
                <Form.Check 
                    type={"checkbox"}
                    id={`${permission}`}
                    name={permission.name}
                    label={`${permission.name}`}
                />
                <p>{permission.description}</p>
                </div>
            )
        }
      })}

      <Button variant="primary" type="submit">
        Edit Role
      </Button>
      <Button className="ms-5" variant="danger" onClick={() => deleteRole(role.id)}>Delete Role</Button>
    </Form>
  )
  

}