import React from 'react';
import OrganizationDataService from '../../services/organization.service'
import { useNavigate } from 'react-router-dom';

export default function App() {
  const [organizations, setOrganizations] = React.useState(null);
  const navigate = useNavigate();

  React.useEffect(() => {
    OrganizationDataService.getAll().then((response) => {
      setOrganizations(response.data);
    }).catch(error => {
      if (error.response.status === 401)
      {
        navigate(`/login`);
        console.log('Not authenticated.');
      }
      if (error.response.status === 403)
      {
        alert('You are not authenticated for this page.');
      }
    });
  }, []);


  if (!organizations) return <p>No data.</p>;

  return (
    <div>
      {organizations.map((organization) => (
        <ul key={organization.id}>
          <h2>{organization.name}</h2>
          
          <li>Twilio Account ID {organization.twilio_account_id}</li>
          <li>Twilio Auth Token {organization.twilio_auth_token}</li>
        </ul>
        
      ))}
    </div>
  );
}