import React from 'react';
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

  const deleteOrganization = () => {

    OrganizationDataService.delete(organization.id).then((response) => {
      navigate(`/organization`);

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

  if (!organization) return <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>

  return (
    <Form onSubmit={handleSubmit} id="organizationForm">

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


      <EditFormDialogModal buttonName="Edit Organization" modalTitle="Edit Organization" modalBody="Are you sure you want to change this organization?"
        form="organizationForm"/>
      <DeleteDialogModal buttonName="Delete Organization" modalTitle="Delete Organization" 
      modalBody="Are you sure you want to delete this organization? This action cannot be reversed." onSuccess={deleteOrganization}/>

    </Form>
  )
  

}