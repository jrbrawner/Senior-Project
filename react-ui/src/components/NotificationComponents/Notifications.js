import React from 'react';
import UserDataService from '../../services/user.service';
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";
import ListGroup from 'react-bootstrap/ListGroup';

export default function Notifications() {
  const [users, setUsers] = React.useState(null);
  
  React.useEffect(() => {
    UserDataService.getAll().then((response) => {
      setUsers(response.data);
    }).catch(error => {
      if (error.response.status === 401)
      {
        //navigate(`/login`);
        console.log('Not authenticated.');
      }
    });
  }, []);

  function banana(){}

  const columns = [
    {
      dataField: "name",
      text: "User Name",
      isDummyField: true,
      formatter: (cellContent, row) => {
        return <ListGroup.Item key={row.id} action onClick={() => banana()} href={`#${row.id}`}>
                  {row.name}
                </ListGroup.Item>
      }
    }
  ]

  if (!users ) return <p>Loading...</p>

  return (
    <div className="sm">
        <ListGroup>
        <BootstrapTable
          bootstrap4
          keyField="id"
          data={users}
          columns={columns}
          pagination={paginationFactory({ sizePerPage: 10 })}
          />
        </ListGroup>
      
      </div>
  );
}