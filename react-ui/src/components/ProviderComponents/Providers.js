import React from 'react';
import ProviderDataSerivce from '../../services/provider.service'

//const baseURL = "http://127.0.0.1:5000/api";

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
        <div>{provider.name}{provider.id}{provider.offices}</div>
      ))}
    </div>
  );
}