import React from 'react';
import OrganizationDataService from '../../services/organization.service';
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';

export default function App() {

  const [organization, setOrganization] = React.useState(null);

  const params = useParams();
  const navigate = useNavigate(); 

  React.useEffect(() => {
    OrganizationDataService.get(params.organizationId).then((response) => {
      setOrganization(response.data);
      
    });
  }, []);

  const handleSubmit = e => {
    e.preventDefault()
    const formData = new FormData(e.target);
    
    OrganizationDataService.update(params.organizationId, formData).then((response) =>
    {
      if (response.status == 200){
          navigate('/organization');
      }
      else{
        alert('Error');
      }
      
    })
  }

  function deleteOrganization(organizationId) {
    OrganizationDataService.delete(organizationId).then((response) =>
    {
      if (response.status === 200){
          navigate('/role');
      }
      else{
        alert("Error");
      }
      
    })
  }

  if (!organization) return <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>

  return (
    <Form onSubmit={handleSubmit}>

      <Form.Group className="mb-3" controlId="formOrgName">
        <Form.Label>Organization Name</Form.Label>
        <Form.Control
            required
            autoComplete="off"
            type="text"
            name="name"
            defaultValue={organization.name}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationAddress">
        <Form.Label>Organization Twilio Account ID</Form.Label>
        <Form.Control
            required
            autoComplete="off"
            type="text"
            name="twilio_account_id"
            defaultValue={organization.twilio_account_id}
          />
      </Form.Group>
      <Form.Group className="mb-3" controlId="formLocationAddress">
        <Form.Label>Organization Twilio Auth Token</Form.Label>
        <Form.Control
            required
            autoComplete="off"
            type="text"
            name="twilio_auth_token"
            defaultValue={organization.twilio_auth_token}
          />
      </Form.Group>


      <Button variant="primary" type="submit">
        Edit Organization
      </Button>
      <Button className="ms-5" variant="danger" onClick={() => deleteOrganization(organization.id)}>Delete Organization</Button>
    </Form>
  )
  

}