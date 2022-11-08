import React from 'react';
import { useNavigate } from 'react-router-dom';
import RoleDataService from '../../services/role.service';
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";
import Spinner from 'react-bootstrap/Spinner';
import Button from 'react-bootstrap/Button';

export default function App() {

    const navigate = useNavigate();
    const [roles, setRoles ] = React.useState();
    const [permissions, setPermissions] = React.useState();

    React.useEffect(() => {
        RoleDataService.getAll().then((response) => {
            setRoles(response.data);
            }).catch(function (error) {
              if (error.response)
              {
                  if (error.response.status === 401)
                  {
                    navigate(`/login`);
                    console.log('Not authenticated.');
                  }
                  if (error.response.status === 403)
                  {
                    alert('You are not authenticated for this page.');
                  }
                  if (error.response.status === 500){
                    navigate(`/login`);
                    console.log('Not authenticated.');
                  }
              }
              });
        }, []);

        function editRole(id) {
            navigate(`/role/${id}`);
          }

        const columns = [
            {
              dataField: "id",
              text: "Role ID",
              sort: true
            },
            {
              dataField: "name",
              text: "Role Name",
              sort: true
            },
            {
              dataField: "description",
              text: "Role Description",
              sort: true
            },
            {
                text: "Edit & Manage Permissions",
                isDummyField: true,
                formatter: (cellContent, row) => {
                  return <Button variant="primary" onClick={() => editRole(row.id)}>Edit</Button>
                }
                
              }
        ]

        if (!roles) return <Spinner animation="border" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </Spinner>

    return (
        <div>
      <div className="mb-1" >
        <Button variant="outline-success">Create New Role</Button>
      </div>
      <BootstrapTable
          bootstrap4
          striped
          bordered
          hover
          keyField="id"
          data={roles}
          columns={columns}
          pagination={paginationFactory({ sizePerPage: 15 })}
          />
    </div>



    )

}