import React from 'react';
import OrganizationDataService from '../../services/organization.service'

export default function App() {
  const [organizations, setOrganizations] = React.useState(null);

  React.useEffect(() => {
    OrganizationDataService.getAll().then((response) => {
      setOrganizations(response.data);
      console.log(response.data)
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