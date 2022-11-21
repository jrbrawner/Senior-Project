import React from 'react';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';
import UserDataService from '../../services/user.service';
import EditFormDialogModal from '../DialogModals/EditFormDialogModal';
import Toast from 'react-bootstrap/Toast';

export default function Password(){

    const navigate = useNavigate();
    const [show, setShow] = React.useState(false);
    const [show1, setShow1] = React.useState(false);

    const handlePasswordChange = e => {
        e.preventDefault();
        const formData = new FormData(e.target);
        var newp = formData.get('newPassword');
        var confp = formData.get('confirmPassword');

        if(newp === confp){

            UserDataService.changePassword(formData).then((response) => {
                navigate(`/profile`);
                console.log(response.status);
                
                }).catch(function (error) {
                  if (error.response)
                    
                    {
                        if (error.response.status === 400)
                        {
                            setShow1(true);
                
                        }
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
        
        else{
            setShow(true);
        }
    }
    
    return (
    <div>

    <Toast onClose={() => setShow(false)} show={show} delay={3000} autohide>
          <Toast.Body>New Password and Confirm New Password must match!</Toast.Body>
    </Toast>
    <Toast onClose={() => setShow1(false)} show={show1} delay={3000} autohide>
          <Toast.Body>Incorrect current password.</Toast.Body>
    </Toast>

    <Form onSubmit={handlePasswordChange} id="passwordForm">
            
                <Form.Group className="mb-3" controlId="formCurrentPassword">
                    <Form.Label>Current Password</Form.Label>
                    <Form.Control
                        required
                        type="password"
                        name="currentPassword"
                        defaultValue=""
                        />
                </Form.Group>
            
                <Form.Group className="mb-3" controlId="formNewPassword">
                    <Form.Label>New Password</Form.Label>
                    <Form.Control
                        required
                        type="password"
                        name="newPassword"
                        defaultValue=""
                        />
                </Form.Group>
            
                <Form.Group className="mb-3" controlId="formConfirmPassword">
                    <Form.Label>Confirm New Password</Form.Label>
                    <Form.Control
                        required
                        type="password"
                        name="confirmPassword"
                        defaultValue=""
                        />
                </Form.Group>
            
                
            <EditFormDialogModal className="-5" buttonName="Change Password" modalTitle="Change Password"
                modalBody="Are you sure you want to change your password?"
                form="passwordForm"/>
                </Form>
    </div>
        )
}