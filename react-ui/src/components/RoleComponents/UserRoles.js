import React from 'react';
import UserDataService from '../../services/user.service';
import RoleDataService from '../../services/role.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';
import OrganizationDataService from '../../services/organization.service';
import EditFormDialogModal from '../DialogModals/EditFormDialogModal';

export default function App() {
  const [user, setUser] = React.useState(null);
  const [roles, setRoles] = React.useState(null);
  const [locations, setLocations] = React.useState(null);

  const navigate = useNavigate(); 
  const params = useParams();
  
  
  React.useEffect(() => {
    UserDataService.get(params.userId).then((response) => {
      setUser(response.data);
      const userLocationId = response.data['location_id'];
      OrganizationDataService.getLocations(response.data['organization_id']).then((response) =>{
        setLocations(response.data);
        
      });
    });
    RoleDataService.getAll().then((response) => {
        setRoles(response.data);
    });
    
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
  if (!locations) return <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </Spinner>
  

  return (
    <Form onSubmit={handleEditSubmit} id="userForm">

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

      <h4>Users Organization Locations</h4>
      {locations.map((location) => {
        if (user.locations.some((x) => x.name === location.name)){
            return (
                <div>
                <Form.Check 
                    type={"checkbox"}
                    defaultChecked={true}
                    id={`${location.name}`}
                    name={location.name}
                    label={`${location.name}`}
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
                    id={`${location.name}`}
                    name={location.name}
                    label={`${location.name}`}
                    />
                </div>
            )
        }
      })}
      <h4>User Roles</h4>
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

      
      <EditFormDialogModal buttonName="Edit User" modalTitle="Edit User" modalBody="Are you sure you want to change this users roles and locations?"
      form="userForm"/>
    </Form>
  )
  
    
}