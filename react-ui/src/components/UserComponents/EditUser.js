import React from 'react';
import UserDataService from '../../services/user.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';
import EditFormDialogModal from '../DialogModals/EditFormDialogModal';
import DeleteDialogModal from '../DialogModals/DeleteDialogModal';
import Spinner from 'react-bootstrap/Spinner';

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

  const deleteUser = () => {

    UserDataService.delete(user.id).then((response) => {
      navigate(`/user`);

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

  if (!user)  return (<Spinner animation="border" role="status">
  <span className="visually-hidden">Loading...</span>
</Spinner>)

  return (
    <Form onSubmit={handleEditSubmit} id="userForm">

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

      <div className="mb-3">
      {user.locations.map((location) => {

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
      })}
      </div>

      <EditFormDialogModal className="-5" buttonName="Edit User" modalTitle="Edit User" modalBody="Are you sure you want to change this user?"
      form="userForm"/>
      <DeleteDialogModal buttonName="Delete User" modalTitle="Delete User" 
      modalBody="Are you sure you want to delete this user? This action cannot be reversed." onSuccess={deleteUser}/>
    </Form>
  )
  

}