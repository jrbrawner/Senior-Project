import React from 'react';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';
import EditFormDialogModal from '../DialogModals/EditFormDialogModal';
import OrganizationDataService from '../../services/organization.service';

export default function App() {

  const navigate = useNavigate();

  const handleSubmit = e => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    OrganizationDataService.create(formData).then((response) => {
        navigate(`/organization`);
        }).catch(function (error) {
          if (error.response)
            {
                if (error.response.status === 401){
                    navigate(`/login`);
                    console.log('Not authenticated.');
                }
                if (error.response.status === 403){
                    alert('You are not authorized for this functionality.');
                }
                
            }
    });
  }

        return (
            <Form onSubmit={handleSubmit} id="newOrgForm">
                <Form.Group className="mb-3" controlId="formOrgName">
                    <Form.Label>Organization Name</Form.Label>
                    <Form.Control
                        required
                        type="text"
                        name="name"
                        defaultValue=""
                    />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formOrgTwilioAccountID">
                    <Form.Label>Organization Account ID</Form.Label>
                    <Form.Control
                        required
                        type="text"
                        name="twilio_account_id"
                        defaultValue=""
                    />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formTwilioAuthToken">
                    <Form.Label>Organization Auth Token</Form.Label>
                    <Form.Control
                        required
                        type="text"
                        name="twilio_auth_token"
                        defaultValue=""
                    />
                </Form.Group>

      <EditFormDialogModal buttonName="Create Organization" modalTitle="Create Organization" modalBody="Are you sure you want to create a new organization?"
      form="newOrgForm"/>
    </Form>
  

    )
}
  


  

