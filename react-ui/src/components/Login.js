import Body from '../components/Body';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import AuthDataService from '../services/auth.service';
import { useNavigate } from 'react-router-dom';

export default function LoginPage(){
    
    const navigate = useNavigate(); 
    
    const handleLoginSubmit = e => {
        
    e.preventDefault();
    const formData = new FormData(e.target);
    const formDataObj = Object.fromEntries(formData.entries());
    console.log(formDataObj);

    AuthDataService.login(formData).then((response) =>
    {
        if (response.status === 200){
            navigate(`/user`);
            //setLoggedIn(LoggedIn = "Yes");
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
