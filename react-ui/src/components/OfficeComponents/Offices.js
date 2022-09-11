import React from 'react';
import OfficeDataService from '../../services/office.service';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import {useNavigate} from 'react-router-dom';

export default function App() {
  const [offices, setOffices] = React.useState(null);
  const navigate = useNavigate();
  
  React.useEffect(() => {
    OfficeDataService.getAll().then((response) => {
      setOffices(response.data);
    });
  }, []);

  function editOffice(id) {
      navigate(`/office/${id}`);

    }
  

  if (!offices) return null;

  return (
    <div>
        <Table striped bordered hover>
          <thead>
            <tr>
                <th>Office Name</th>
                <th>Address</th>
                <th>City</th>
                <th>State</th>
                <th>Phone Number</th>
                <th>Physicians</th>
                <th>Edit</th>
                <th>Delete</th>
            </tr>
          </thead>
            <tbody>
            {offices.map((office) => (
            <tr key={office.id}>
                <td>{office.name}</td>
                <td>{office.address}</td>
                <td>{office.city}</td>
                <td>{office.state}</td>
                <td>{office.phone_number}</td>
                <td></td>
                <td><Button variant="primary" onClick={() => editOffice(office.id)}>Edit</Button>{' '}</td>
                <td><Button variant="danger">Delete</Button>{' '}</td>
            </tr>
                ))}
            </tbody>
      </Table>
      
    </div>
  );
}