import React from 'react';
import OfficeDataService from '../../services/office.service'
import Table from 'react-bootstrap/Table'

export default function App() {
  const [offices, setOffices] = React.useState(null);

  React.useEffect(() => {
    OfficeDataService.getAll().then((response) => {
      setOffices(response.data);
    });
  }, []);

  if (!offices) return null;

  return (
    <div>
        <Table striped bordered hover>
            <tr>
                <th>Office Name</th>
                <th>Address</th>
                <th>City</th>
                <th>State</th>
                <th>Phone Number</th>
                <th>Physicians</th>
            </tr>
            <tbody>
            {offices.map((office) => (
            <tr key={office.id}>
                <td>{office.name}</td>
                <td>{office.address}</td>
                <td>{office.city}</td>
                <td>{office.state}</td>
                <td>{office.phone_number}</td>
                <td></td>
            </tr>
                ))}
            </tbody>
      </Table>
      
    </div>
  );
}