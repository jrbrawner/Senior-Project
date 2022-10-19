import React from "react";
import { Button, Badge, ListGroup, Stack } from "react-bootstrap";
import MessageDataService from '../services/message.service';
import { useNavigate } from 'react-router-dom';

export default function Sidebar(props) {

  
  const navigate = useNavigate();

  const locations = props.locations;
  const selectedUserMessages = props.selectedUserMessages;
  const users = props.users;
  const loadPeople = props.loadPeople;

  
    if (!users){
      return (
      <Stack gap={3}>
          
          <h5>Locations</h5>
          <ListGroup>
            {locations.map((location) => (
              
              <ListGroup.Item key={location.id} variant="light" action href={() => loadPeople(location.id)}>
                {location.name} <Badge bg="success">2</Badge>
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
      <ListGroup>
        {locations.map((location) => (
          
          <ListGroup.Item key={location.id} variant="light" action href={() => loadPeople(location.id)}>
            {location.name} <Badge bg="success">2</Badge>
          </ListGroup.Item>

))}
      </ListGroup>

      <h5>Patients</h5>

      <ListGroup defaultActiveKey="">

      {users.map((user) =>(
        <ListGroup.Item key={user.id} variant="light" action href={() => selectedUserMessages(user.id)}>
          {user.name}
        </ListGroup.Item>
        ))}

      </ListGroup>

    </Stack>
    )
}
  