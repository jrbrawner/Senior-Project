import React from 'react';
import MessageDataService from '../../services/message.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';

export default function App(){

    const params = useParams();
    const navigate = useNavigate(); 

    const handleSubmit = e => {
        e.preventDefault();
        const formData = new FormData(e.target);

        MessageDataService.sendAnnouncement(params.locationId, formData).then((response) => {
            alert('Announcement sent.')
            navigate('/location');
        }).catch(error => {
            if (error.response.status === 401)
            {
            navigate(`/login`);
            console.log('Not authenticated.');
            }
        });
        
    }

    return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="formLocationName">
        <Form.Label>Message to send</Form.Label>
        <Form.Control
            required
            type="text"
            name="msg"
            defaultValue=""
          />
      </Form.Group>

      <Button variant="primary" type="submit">
        Send Announcement
      </Button>
    </Form>
    )
}