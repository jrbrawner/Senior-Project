import React from 'react';
import { useNavigate } from 'react-router-dom';
import RoleDataService from '../../services/role.service';
import BootstrapTable from "react-bootstrap-table-next";
import UserDataService from "../../services/user.service";
import paginationFactory from "react-bootstrap-table2-paginator";
import Spinner from 'react-bootstrap/Spinner';
import Button from 'react-bootstrap/Button';
import Dropdown from 'react-bootstrap/Dropdown';

export default function App() {

    const navigate = useNavigate();
    const [roles, setRoles ] = React.useState();
    const [users, setUsers] = React.useState();

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
              
              UserDataService.getAll().then((response) => {
                setUsers(response.data);
                
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

        function newRole() {
          navigate(`/role/create`);
        }

        function editUserRoles(id) {
          navigate(`/role/user/${id}`)
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

        const columns1 = [
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
              if (row.roles.length > 1){ return( 
                          <Dropdown>
                          <Dropdown.Toggle variant="" id="dropdown-basic">
                            Roles
                          </Dropdown.Toggle>
                          <Dropdown.Menu>
                            {row.roles.map((role) => (
                              <Dropdown.Item>{role.name}</Dropdown.Item>
                            ))}
                          </Dropdown.Menu>
                        </Dropdown>
                        )
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
              return <Button variant="primary" onClick={() => editUserRoles(row.id)}>Edit</Button>
            }
            
          }
        ]

        

    if (!roles) return <Spinner animation="border" role="status">
                            <span className="visually-hidden">Loading...</span>
                        </Spinner>
    if (!users) return <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>
                  

    return (
      <div>
        <div>
      <div className="mb-1" >
        <Button variant="outline-success" onClick={() => newRole()}>Create New Role</Button>
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

          <div>
          <BootstrapTable
              bootstrap4
              striped
              bordered
              hover
              keyField="id"
              data={users}
              columns={columns1}
              pagination={paginationFactory({ sizePerPage: 15 })}
              />
          </div>
      </div>


    )
}