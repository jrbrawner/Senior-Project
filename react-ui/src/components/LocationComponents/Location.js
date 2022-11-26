import React from 'react';
import LocationDataService from '../../services/location.service'
import { useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import EditFormDialogModal from '../DialogModals/EditFormDialogModal';
import DeleteDialogModal from '../DialogModals/DeleteDialogModal';
import Spinner from 'react-bootstrap/Spinner';

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
    e.preventDefault();
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

  const deleteLocation = () => {

    LocationDataService.delete(location.id).then((response) => {
      navigate(`/location`);

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



  if (!location) return (<Spinner animation="border" role="status">
                                <span className="visually-hidden">Loading...</span>
                        </Spinner>)

  return (
    <Form onSubmit={handleSubmit} id="locationForm">
      <Form.Group className="mb-3" controlId="formLocationName">
        <Form.Label>Location Name</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="name"
            defaultValue={location.name}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationAddress">
        <Form.Label>Address</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="address"
            defaultValue={location.address}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationCity">
        <Form.Label>City</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="city"
            defaultValue={location.city}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationState">
        <Form.Label>State</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="state"
            defaultValue={location.state}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationZipCode">
        <Form.Label>Zip Code</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="zipCode"
            defaultValue={location.zip_code}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationPhoneNumber">
        <Form.Label>Phone Number</Form.Label>
        <Form.Control
            required
            autocomplete="off"
            type="text"
            name="phoneNumber"
            defaultValue={location.phone_number}
          />
      </Form.Group>
      <EditFormDialogModal buttonName="Edit Location" modalTitle="Edit Location" modalBody="Are you sure you want to change this location?"
      form="locationForm"/>
      <DeleteDialogModal buttonName="Delete Location" modalTitle="Delete Location" 
      modalBody="Are you sure you want to delete this location? This action cannot be reversed." onSuccess={deleteLocation}/>

    </Form>
  )
  

}