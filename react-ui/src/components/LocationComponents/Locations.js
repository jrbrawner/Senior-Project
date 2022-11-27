import React from 'react';
import LocationDataService from '../../services/location.service';
import Table from 'react-bootstrap/Table';
import {useNavigate} from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';
import Button from 'react-bootstrap/Button';
import paginationFactory from "react-bootstrap-table2-paginator";
import BootstrapTable from "react-bootstrap-table-next";

export default function App() {
  const [locations, setLocations] = React.useState(null);
  const navigate = useNavigate();
  
  React.useEffect(() => {
  
      LocationDataService.getAll().then((response) => {
        setLocations(response.data);
        }).catch(function (error) {
          if (error.response)
            {
                if (error.response.status === 401){
                    navigate(`/login`);
                    console.log('Not authenticated.')
                }
            }
    });
  }, []);

  function editLocation(id) {
      navigate(`/location/${id}`);
    }

  function announcementPage(id) {
    navigate(`/location/${id}/announcement`)
  }

  function newLocation(){
    navigate(`/location/create`)
  }
  

  const columns = [
    {
      dataField: "organization_name",
      text: "Organization",
      sort: true
    },
    {
      dataField: "name",
      text: "Location Name",
      sort: true
    },
    {
      dataField: "address",
      text: "Address",
      sort: true
    },
    {
      dataField: "city",
      text: "City",
      sort: true
    },
    {
      dataField: "state",
      text: "State",
      sort: true
    },
    {
      dataField: "phone_number",
      text: "Phone Number",
      sort: true
    },
    {
      text: "Edit Location",
      isDummyField: true,
      formatter: (cellContent, row) => {
        return <Button variant="primary" onClick={() => editLocation(row.id)}>Edit</Button>
      }
      
    },
    {
      text: "Send Announcement",
      isDummyField: true,
      formatter: (cellContent, row) => {
        return <Button variant="info" onClick={() => announcementPage(row.id)}>Send Announcement</Button>
      }
      
    }
  ]


  if (!locations) return <Spinner animation="border" role="status">
                              <span className="visually-hidden">Loading...</span>
                            </Spinner>

  return (
    <div>
      <div className="mb-1" >
        <Button variant="outline-success" onClick={() => newLocation()}>Create New Location</Button>
      </div>
      <BootstrapTable
          bootstrap4
          striped
          bordered
          hover
          keyField="id"
          data={locations}
          columns={columns}
          pagination={paginationFactory({ sizePerPage: 15 })}
          />
    </div>
  );
}