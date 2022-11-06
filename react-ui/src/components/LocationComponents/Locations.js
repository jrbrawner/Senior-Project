import React from 'react';
import LocationDataService from '../../services/location.service';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import {useNavigate} from 'react-router-dom';

export default function App() {
  const [locations, setLocations] = React.useState(null);
  const navigate = useNavigate();
  
  React.useEffect(() => {
    LocationDataService.getAll().then((response) => {
      setLocations(response.data);
    }).catch(error => {
      if (error.response.status === 401){
        navigate(`/login`);
        console.log('Not authenticated.');
      }});
  }, []);

  function editLocation(id) {
      navigate(`/location/${id}`);
    }

  function announcementPage(id) {
    navigate(`/location/${id}/announcement`)
  }
  

  if (!locations) return null;

  return (
    <div>
        <Table striped bordered hover>
          <thead>
            <tr>
                <th>Location Name</th>
                <th>Address</th>
                <th>City</th>
                <th>State</th>
                <th>Phone Number</th>
                <th>Edit</th>
                <th>Announcement</th>
            </tr>
          </thead>
            <tbody>
            {locations.map((location) => (
            <tr key={location.id}>
                <td>{location.name}</td>
                <td>{location.address}</td>
                <td>{location.city}</td>
                <td>{location.state}</td>
                <td>{location.phone_number}</td>
                <td><Button variant="primary" onClick={() => editLocation(location.id)}>Edit</Button>{' '}</td>
                <td><Button variant="info" onClick={() => announcementPage(location.id)}>Announcement</Button>{' '}</td>
            </tr>
                ))}
            </tbody>
      </Table>
      
    </div>
  );
}