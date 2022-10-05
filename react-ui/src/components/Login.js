import Body from '../components/Body';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import AuthDataService from '../services/auth.service';
import { useNavigate } from 'react-router-dom';
import React from 'react';
import { useSelector, useDispatch, connect } from 'react-redux';
import {setName, setLoggedIn} from '../store/userSlice';

const LoginPage = ({setUserName, name}) => {

        const navigate = useNavigate();
        const dispatch = useDispatch();
        //const selector = useSelector();

        const handleLoginSubmit = e => {

        e.preventDefault();
        const formData = new FormData(e.target);
        //const formDataObj = Object.fromEntries(formData.entries());
        //console.log(formDataObj);

        AuthDataService.login(formData).then((response) =>
        {
            if (response.status === 200){
                navigate(`/user`);
                dispatch(setUserName(response.data['msg']));
                dispatch(setLoggedIn(true));
                
            }
            if (response.status === 400){
                alert("Error");
            }
            
        });
    }
        return (
            <Body >
            <Form onSubmit={handleLoginSubmit}>
            
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
const actions = {
    setUserName: setName
}

const select = state => ({
    name: state.user.name
})

export default connect(select, actions)(LoginPage)