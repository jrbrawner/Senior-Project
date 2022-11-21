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
import OrganizationDataService from '../../services/organization.service';
import Cookies from 'js-cookie';

export default function App() {

  const [organizations, setOrganizations] = React.useState();
  const navigate = useNavigate();

  const state = {
    username: Cookies.get('name'),
    roles: Cookies.get('roles')
  }

  React.useEffect(() => {
    if (state.roles != undefined){
        if(state.roles.includes('Super Admin')){

            OrganizationDataService.getAll().then((response) => {
                setOrganizations(response.data);
                }).catch(function (error) {
                  if (error.response)
                    {
                        if (error.response.status === 401){
                            navigate(`/login`);
                            console.log('Not authenticated.')
                        }
                        if (error.response.status === 403){
                            alert('You are not authorized for this functionality.')
                        }
                        if (error.response.status === 500){
                            navigate(`/login`);
                            console.log('Not authenticated.');
                          }
                    }
                });
            }
        }
    }, []);

  const handleSubmit = e => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    LocationDataService.create(formData).then((response) => {
        navigate(`/location`);
        }).catch(function (error) {
          if (error.response)
            {
                if (error.response.status === 401){
                    navigate(`/login`);
                    console.log('Not authenticated.');
                }
                if (error.response.status === 403){
                    alert('You are not authorized for this functionality.');
                }
                
            }
    });
  }

  if(state.roles != undefined){
    if(state.roles.includes('Super Admin')){
        

        if (!organizations) return <Spinner animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
        </Spinner>

        return (
            <Form onSubmit={handleSubmit} id="newlocationForm">
      <Form.Group className="mb-3" controlId="formLocationName">
        <Form.Label>Location Name</Form.Label>
        <Form.Control
            required
            type="text"
            name="name"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationAddress">
        <Form.Label>Address</Form.Label>
        <Form.Control
            required
            type="text"
            name="address"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationCity">
        <Form.Label>City</Form.Label>
        <Form.Control
            required
            type="text"
            name="city"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationState">
        <Form.Label>State</Form.Label>
        <Form.Control
            required
            type="text"
            name="state"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationZipCode">
        <Form.Label>Zip Code</Form.Label>
        <Form.Control
            required
            type="text"
            name="zipCode"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationPhoneNumber">
        <Form.Label>Phone Number</Form.Label>
        <Form.Control
            required
            type="text"
            name="phoneNumber"
            defaultValue=""
          />
      </Form.Group>
      
      
      <Form.Label>Select Organization For This Location</Form.Label>
        {organizations.map((organization) => {
        return (
            <div>
            <Form.Check 
                type={"checkbox"}
                defaultChecked={false}
                id={`${organization.name}`}
                name={organization.name}
                label={`${organization.name}`}
                />
            </div>
        )
        })}
      <EditFormDialogModal buttonName="Create Location" modalTitle="Create Location" modalBody="Are you sure you want to create a new location?"
      form="newlocationForm"/>
    </Form>
  

        )
    }
  }

  return (
    <Form onSubmit={handleSubmit} id="newlocationForm">
      <Form.Group className="mb-3" controlId="formLocationName">
        <Form.Label>Location Name</Form.Label>
        <Form.Control
            required
            type="text"
            name="name"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationAddress">
        <Form.Label>Address</Form.Label>
        <Form.Control
            required
            type="text"
            name="address"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationCity">
        <Form.Label>City</Form.Label>
        <Form.Control
            required
            type="text"
            name="city"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationState">
        <Form.Label>State</Form.Label>
        <Form.Control
            required
            type="text"
            name="state"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationZipCode">
        <Form.Label>Zip Code</Form.Label>
        <Form.Control
            required
            type="text"
            name="zipCode"
            defaultValue=""
          />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formLocationPhoneNumber">
        <Form.Label>Phone Number</Form.Label>
        <Form.Control
            required
            type="text"
            name="phoneNumber"
            defaultValue=""
          />
      </Form.Group>
      
      <EditFormDialogModal buttonName="Create Location" modalTitle="Create Location" modalBody="Are you sure you want to create a new location?"
      form="newlocationForm"/>
    </Form>
  )
  

}