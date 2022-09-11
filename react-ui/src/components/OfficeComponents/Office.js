import React from 'react';
import OfficeDataService from '../../services/office.service'
import {useParams} from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

export default function App() {
  const [office, setOffice] = React.useState(null);

  const params = useParams();

  React.useEffect(() => {
    OfficeDataService.get(params.officeId).then((response) => {
      setOffice(response.data);
    });
  }, []);

  const handleSubmit = e => {
    e.preventDefault()
    const formData = new FormData(e.target);
    formData.append('providerId', office.provider_id);
    const formDataObj = Object.fromEntries(formData.entries());
    console.log(formDataObj);
    OfficeDataService.update(params.officeId, formData);
  }

  if (!office) return null;

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="formOfficeName">
        <Form.Label>Office Name</Form.Label>
        <Form.Control
            required
            type="text"
            name="name"
            defaultValue={office.name}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formOfficeAddress">
        <Form.Label>Address</Form.Label>
        <Form.Control
            required
            type="text"
            name="address"
            defaultValue={office.address}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formOfficeCity">
        <Form.Label>City</Form.Label>
        <Form.Control
            required
            type="text"
            name="city"
            defaultValue={office.city}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formOfficeState">
        <Form.Label>State</Form.Label>
        <Form.Control
            required
            type="text"
            name="state"
            defaultValue={office.state}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formOfficeZipCode">
        <Form.Label>Zip Code</Form.Label>
        <Form.Control
            required
            type="text"
            name="zipCode"
            defaultValue={office.zip_code}
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formOfficePhoneNumber">
        <Form.Label>Phone Number</Form.Label>
        <Form.Control
            required
            type="text"
            name="phoneNumber"
            defaultValue={office.phone_number}
          />
      </Form.Group>
      <Button variant="primary" type="submit">
        Edit Office
      </Button>
    </Form>
  )
  

}