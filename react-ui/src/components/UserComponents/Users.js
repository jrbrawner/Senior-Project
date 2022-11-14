import React from 'react';
import UserDataService from '../../services/user.service';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import {useNavigate} from 'react-router-dom';
import Dropdown from 'react-bootstrap/Dropdown';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

export default function App() {
  
  const [users, setUsers] = React.useState(null);
  const navigate = useNavigate();
  
  React.useEffect(() => {
    UserDataService.getAll().then((response) => {
      setUsers(response.data);
    }).catch(error => {
      if (error.response.status === 401)
      {
        navigate(`/login`);
        console.log('Not authenticated.');
      }
    });
  }, []);
  
  function editUser(id) {
    navigate(`/user/${id}`);
  }

  function newUser() {
    navigate(`/user/create`);
  }

  const columns = [
    {
      dataField: "name",
      text: "User Name",
      sort: true
    },
    {
      dataField: "email",
      text: "User Email",
      sort: true
    },
    {
      dataField: "locations.name",
      text: "User Locations",
      sort:true,
      formatter: (cellContent, row) => {
        if (row.locations.length > 1){ return <Dropdown>
                    <Dropdown.Toggle variant="" id="dropdown-basic">
                      Locations
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                      {row.locations.map((location) => (
                        <Dropdown.Item>{location.name}</Dropdown.Item>
                      ))}
                    </Dropdown.Menu>
                  </Dropdown>
                  }
        else
        {
          return <td>{row.locations.map((location) => (
                      location.name))}</td>
          }
      }
    },
    {
      dataField: "roles.name",
      text: "User Role",
      sort:true,
      formatter: (cellContent, row) => {
        if (row.roles.length > 1){ return <Dropdown>
                    <Dropdown.Toggle variant="" id="dropdown-basic">
                      Roles
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                      {row.roles.map((role) => (
                        <Dropdown.Item>{role.name}</Dropdown.Item>
                      ))}
                    </Dropdown.Menu>
                  </Dropdown>
                  }
        else
        {
          return <td>{row.roles.map((role) => (
                      role.name))}</td>
          }
      }
    },
    {
      dataField: "phone_number",
      text: "User Phone Number",
      sort:true
    },
    {
      text: "Edit User",
      isDummyField: true,
      formatter: (cellContent, row) => {
        return <Button variant="primary" onClick={() => editUser(row.id)}>Edit</Button>
      }
      
    }
  ]

  if (!users) return <p>Loading</p>;

  return (

    
    <div>
      <div className="mb-1" >
        <Button variant="outline-success" onClick={() => newUser()}>Create New User</Button>
      </div>
      <BootstrapTable
          bootstrap4
          striped
          bordered
          hover
          keyField="id"
          data={users}
          columns={columns}
          pagination={paginationFactory({ sizePerPage: 10 })}
          />
    </div>
  );
}