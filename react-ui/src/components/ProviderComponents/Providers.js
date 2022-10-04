import React from 'react';
import ProviderDataSerivce from '../../services/provider.service'

export default function App() {
  const [providers, setProviders] = React.useState(null);

  React.useEffect(() => {
    ProviderDataSerivce.getAll().then((response) => {
      setProviders(response.data);
      //console.log(response.data)
    });
  }, []);

  if (!providers) return null;

  return (
    <div>
      {providers.map((provider) => (
        <ul key={provider.id}>
          <h2>{provider.name}</h2>
          <li>{provider.offices}</li>
          <li>{provider.twilio_account_id}</li>
          <li>{provider.twilio_auth_token}</li>
        </ul>
        
      ))}
    </div>
  );
}