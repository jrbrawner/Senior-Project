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
    }).catch(error => {
      if (error.response.status === 401){
        navigate(`/login`);
        console.log('Not authenticated.');
      }});
  }, []);

  function editUser(id) {
      navigate(`/user/${id}`);
    }
  function newUser() {
    navigate(`/user/create`);
  }

  function deleteUser(userId) {
    UserDataService.delete(userId).then((response) =>
    {
      if (response.status === 200){
          navigate(0);
      }
      else{
        alert("Error");
      }
      
    })
  }

  if (!users) return <p>Loading</p>;

  return (
    <div>
      <div className="mb-1" >
        <Button variant="outline-success" onClick={() => newUser()}>Create New User</Button>
      </div>

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
                <td><Button variant="danger" onClick={() => deleteUser(user.id)}>Delete</Button>{' '}</td>
            </tr>
                ))}
            </tbody>
      </Table>
      
    </div>
  );
}