import React from 'react';
import UserDataService from '../../services/user.service';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import {useNavigate} from 'react-router-dom';

export default function App() {
  
  const [users, setUsers] = React.useState(null);
  const navigate = useNavigate();
  
  React.useEffect(() => {
    UserDataService.getPending().then((response) => {
      setUsers(response.data);
    }).catch(error => {
      if (error.response.status === 401)
      {
        navigate(`/login`);
        console.log('Not authenticated.');
      }
    });
  }, []);

  function acceptUser(userId) {
    UserDataService.acceptPending(userId).then((response) =>
    {
      if (response.status === 200){
          navigate('/user');
      }
      else{
        alert("Error");
      }
      
    })
    }
  

  function declineUser(userId) {
    UserDataService.declinePending(userId).then((response) =>
    {
      if (response.status === 200){
          navigate('/user');
      }
      else{
        alert("Error");
      }
      
    })
  }

  if (!users) return <p>Loading</p>;

  return (
    <div>
        <Table striped bordered hover>
          <thead>
            <tr>
                <th>User Name</th>
                <th>User Email</th>
                <th>User Location</th>
                <th>Phone Number</th>
                <th>Accept</th>
                <th>Decline</th>
            </tr>
          </thead>
            <tbody>
            {users.map((user) => (
            <tr key={user.id}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.location_name}</td>
                
                <td>{user.phone_number}</td>
                <td><Button variant="success" onClick={() => acceptUser(user.id)}>Accept</Button>{' '}</td>
                <td><Button variant="danger" onClick={() => declineUser(user.id)}>Decline</Button>{' '}</td>
            </tr>
                ))}
            </tbody>
      </Table>
      
    </div>
  );
}