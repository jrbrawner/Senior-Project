import React from 'react';
import UserDataService from '../../services/user.service';
import { useNavigate } from 'react-router-dom';
import EditFormDialogModal from '../DialogModals/EditFormDialogModal';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Toast from 'react-bootstrap/Toast';

export default function App(){

    const [user, setUser] = React.useState(null);
    const [show, setShow] = React.useState(false);
    const navigate = useNavigate();

    React.useEffect(() => {
        UserDataService.getProfile().then((response) => {
  
            setUser(response.data);
            
            }).catch(function (error) {
              if (error.response)
              {
                  if (error.response.status === 401)
                  {
                    navigate(`/login`);
                    console.log('Not authenticated.');
          
                  }
                  if (error.response.status === 403)
                  {
                    alert('You are not authenticated for this page.');
                  }
                  if (error.response.status === 500){
                    navigate(`/login`);
                    console.log('Not authenticated.');
                  }
              }
              });
        
        }, []);

    const handleEditSubmit = e => {
        e.preventDefault();
        const formData = new FormData(e.target);
        formData.append('userId', user.id);
        console.log(formData);
        
        UserDataService.editProfile(formData).then((response) => {
            navigate(`/profile`);
            setShow(true);
            console.log(response.status);
            
            }).catch(function (error) {
              if (error.response)
                
                {
                    if (error.response.status === 401)
                    {
                        navigate(`/login`);
                        console.log('Not authenticated.');
            
                    }
                    if (error.response.status === 403)
                    {
                        alert('You are not authenticated for this page.');
                    }
                    if (error.response.status === 500){
                        navigate(`/login`);
                        console.log('Not authenticated.');
                    }

                }
        });
        }

    function changePassword(){
        navigate(`/profile/password`);
    }

        
        
        if (!user)  return (<Spinner animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>)
      
      return (
    <Container>
        <Row>
            <Col>
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
                        disabled
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
                <h5>Locations</h5>
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
            
                <EditFormDialogModal className="-5" buttonName="Edit Info" modalTitle="Edit Profile Information"
                 modalBody="Are you sure you want to update your profile information?"
                form="userForm"/>
                </Form>

                <Button className="mt-2"  variant="success" onClick={() => changePassword()}>Change password</Button>

            </Col>
            <Col>
            <Toast onClose={() => setShow(false)} show={show} delay={3000} autohide>
            <Toast.Body>Profile Updated</Toast.Body>
            </Toast>
            </Col>
        </Row>
    </Container>
      )
    
}