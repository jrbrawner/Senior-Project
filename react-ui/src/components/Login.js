import Body from '../components/Body';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import AuthDataService from '../services/auth.service';
import { useNavigate } from 'react-router-dom';
import React from 'react';
import Cookies from 'js-cookie';
import Toast from 'react-bootstrap/Toast';

export default function Login(){

        const navigate = useNavigate();
        const [show, setShow] = React.useState(false);


        const handleLoginSubmit = e => {

        e.preventDefault();
        const formData = new FormData(e.target);

        AuthDataService.login(formData).then((response) => {
            Cookies.set('name', response.data['name']);
                var roles = "";
                response.data['roles'].map((role) =>
                {
                    roles += role.name + ",";
                })
                var decodedRoles = decodeURI(roles);
                Cookies.set('roles', decodedRoles);
                //navigate(`/user`);
                window.location.href = '/location';
            
            }).catch(function (error) {
              if (error.response)
                {
                    if (error.response.status === 405){
                        setShow(true);
                    }
                }
        });
    }

        return (
            <Body >
            <Form onSubmit={handleLoginSubmit}>
                <h3>Login to be authenticated and access the portal.</h3>
                <Toast onClose={() => setShow(false)} show={show} delay={3000} autohide>
                    <Toast.Body>Username/Password combination not recognized.</Toast.Body>
                </Toast>
                <Form.Group className="mb-1" controlId="formLoginEmail">
                <Form.Label>Email</Form.Label>
                <Form.Control
                    required
                    type="text"
                    name="email"
                    />
                </Form.Group>

                <Form.Group className="mb-1" controlId="formLoginPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control
                    required
                    type="password"
                    name="password"
                    />
                </Form.Group>
                <Button variant="success" type="submit">
                    Login
                </Button>
            </Form>
        </Body>
    );
    
}