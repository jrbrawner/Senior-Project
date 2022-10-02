import React from 'react';
import UserDataService from '../../services/user.service';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import {useNavigate} from 'react-router-dom';

export default function App() {
  const [users, setUsers] = React.useState(null);
  const navigate = useNavigate();
  
  React.useEffect(() => {
    UserDataService.getAll().then((response) => {
      setUsers(response.data);
    });
  }, []);

  function editUser(id) {
      navigate(`/user/${id}`);

    }
  

  if (!users) return <p>Error.</p>;

  return (
    <div>
        <Table striped bordered hover>
          <thead>
            <tr>
                <th>User Name</th>
                <th>User Email</th>
                <th>User Location</th>
                <th>User Roles</th>
                <th>Phone Number</th>
                <th>Edit</th>
                <th>Delete</th>
            </tr>
          </thead>
            <tbody>
            {users.map((user) => (
            <tr key={user.id}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.location_id}</td>
                <td>{user.roles.map((role) => (
                        role.name))}</td>
                <td>{user.phone_number}</td>
                <td><Button variant="primary" onClick={() => editUser(user.id)}>Edit</Button>{' '}</td>
                <td><Button variant="danger">Delete</Button>{' '}</td>
            </tr>
                ))}
            </tbody>
      </Table>
      
    </div>
  );
}