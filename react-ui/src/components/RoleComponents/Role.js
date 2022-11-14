import React from 'react';
import RoleDataService from '../../services/role.service';
import OrganizationDataService from '../../services/organization.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';
import EditFormDialogModal from '../DialogModals/EditFormDialogModal';
import DeleteDialogModal from '../DialogModals/DeleteDialogModal';

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

  const deleteRole = () => {

    RoleDataService.delete(role.id).then((response) => {
      navigate(`/role`);

    }).catch(error => {
      if (error.response.status === 401)
      {
        navigate(`/login`);
        console.log('Not authenticated.');
      }
      if (error.response.status === 403)
      {
        alert('You are not authenticated for this functionality.');
      }
    });
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
    <Form onSubmit={handleSubmit} id="roleForm">
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

      <EditFormDialogModal buttonName="Edit Role" modalTitle="Edit Role" modalBody="Are you sure you want to change this role?"
      form="roleForm"/>
      <DeleteDialogModal buttonName="Delete Role" modalTitle="Delete Role" 
      modalBody="Are you sure you want to delete this role? This action cannot be reversed." onSuccess={deleteRole}/>
    </Form>
  )
  

}