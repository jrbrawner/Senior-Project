import React from "react";
import { Button, Badge, ListGroup, Stack } from "react-bootstrap";
import MessageDataService from '../services/message.service';
import { useNavigate } from 'react-router-dom';
import Pagination from 'react-bootstrap/Pagination';
import Pager from '../components/PagingComponents/Pager';
import BootstrapTable from "react-bootstrap-table-next";

export default function Sidebar(props) {

  
  const navigate = useNavigate();

  const locations = props.locations;
  const selectedUserMessages = props.selectedUserMessages;
  const users = props.users;
  const loadPeople = props.loadPeople;

  

  const columns = [
    {
      dataField: "name",
      text: "name",
      sort: true
    },
  ];

  
    if (!users){
      return (
      <Stack gap={3}>
          
          <h5>Locations</h5>
          <ListGroup>
            {locations.map((location) => (
              
              <ListGroup.Item key={location.id} variant="light" action href={() => loadPeople(location.id)}>
                {location.name} <Badge bg="success">{location.messages_no_response}</Badge>
              </ListGroup.Item>
  
  ))}
          </ListGroup>


    </Stack>
    );
  }
  else
    return(
      <Stack gap={3}>
          
      <h5>Locations</h5>
      <ListGroup defaultActiveKey="">
        {locations.map((location) => (
          
          <ListGroup.Item key={location.id} action onClick={() => loadPeople(location.id)} variant="light">
            {location.name} <Badge bg="success">{location.messages_no_response}</Badge>
          </ListGroup.Item>

))}
      </ListGroup>

      <h5>Patients</h5>

      <ListGroup defaultActiveKey="">

      {users.map((user) => {

        if (user.unread_msg === 0){
          
          return (
        <ListGroup.Item key={user.id} action onClick={() => selectedUserMessages(user.id)} href={`#${user.id}`}>
          {user.name}
        </ListGroup.Item>
        )}

        else{

          return (
          <ListGroup.Item key={user.id} action onClick={() => selectedUserMessages(user.id)} href={`#${user.id}`}>
          {user.name} <Badge bg="success">{user.unread_msg}</Badge>
          </ListGroup.Item>

        )}

        })}


      </ListGroup>


    </Stack>
    )
}
  