import React from 'react';
import OrganizationDataService from '../../services/organization.service'
import { useNavigate } from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';
import Button from 'react-bootstrap/Button';
import paginationFactory from "react-bootstrap-table2-paginator";
import BootstrapTable from "react-bootstrap-table-next";

export default function App() {
  const [organizations, setOrganizations] = React.useState(null);
  const navigate = useNavigate();

  React.useEffect(() => {
    OrganizationDataService.getAll().then((response) => {
      setOrganizations(response.data);
    }).catch(error => {
      if (error.response.status === 401)
      {
        navigate(`/login`);
        console.log('Not authenticated.');
      }
      if (error.response.status === 403)
      {
        alert('You are not authenticated for this page.');
      }
    });
  }, []);

  function EditOrg(id){
    navigate(`/organization/${id}`)
  }

  const columns = [
    {
      dataField: "name",
      text: "Organization Name",
      sort: true
    },
    {
      dataField: "twilio_account_id",
      text: "Org Twilio Account ID",
      sort: true
    },
    {
      dataField: "twilio_auth_token",
      text: "Org Twilio Auth Token",
      sort: true
    },
    {
      text: "Edit Organization",
      isDummyField: true,
      formatter: (cellContent, row) => {
        return <Button variant="primary" onClick={() => EditOrg(row.id)}>Edit</Button>
      }
      
    }
  ]


  if (!organizations) return <Spinner animation="border" role="status">
                              <span className="visually-hidden">Loading...</span>
                            </Spinner>

  return (
    <div>
      <BootstrapTable
          bootstrap4
          striped
          bordered
          hover
          keyField="id"
          data={organizations}
          columns={columns}
          pagination={paginationFactory({ sizePerPage: 15 })}
          />
    </div>
  );
}