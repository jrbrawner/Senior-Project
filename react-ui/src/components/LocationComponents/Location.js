import React from 'react';
import LocationDataService from '../../services/location.service'
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


export default function App() {
  const [location, setLocation] = React.useState(null);

  const params = useParams();
  const navigate = useNavigate(); 

  React.useEffect(() => {
    LocationDataService.get(params.locationId).then((response) => {
      setLocation(response.data);
    });
  }, []);

  

  const handleSubmit = e => {
    e.preventDefault()
    const formData = new FormData(e.target);
    formData.append('organizationId', location.organization_id);
    const formDataObj = Object.fromEntries(formData.entries());
    console.log(formDataObj);
    LocationDataService.update(params.locationId, formData).then((response) =>
    {
      if (response.status == 200){
          navigate('/location');
      }
      else{
        alert('Error');
      }
      
    })
  }

  if (!location) return null;

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="formLocationName">
        <Form.Label>Location Name</Form.Label>
        <Form.Control
            required
            type="text"
            name="name"
            defaultValue={location.name}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationAddress">
        <Form.Label>Address</Form.Label>
        <Form.Control
            required
            type="text"
            name="address"
            defaultValue={location.address}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationCity">
        <Form.Label>City</Form.Label>
        <Form.Control
            required
            type="text"
            name="city"
            defaultValue={location.city}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationState">
        <Form.Label>State</Form.Label>
        <Form.Control
            required
            type="text"
            name="state"
            defaultValue={location.state}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationZipCode">
        <Form.Label>Zip Code</Form.Label>
        <Form.Control
            required
            type="text"
            name="zipCode"
            defaultValue={location.zip_code}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationPhoneNumber">
        <Form.Label>Phone Number</Form.Label>
        <Form.Control
            required
            type="text"
            name="phoneNumber"
            defaultValue={location.phone_number}
          />
      </Form.Group>
      <Button variant="primary" type="submit">
        Edit location
      </Button>
    </Form>
  )
  

}