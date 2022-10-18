import React from "react";
import { Button, Badge, ListGroup, Stack } from "react-bootstrap";

export default function Sidebar({locations}) {

    return (
      <Stack gap={3}>
          <div>
          <h5>Locations</h5>
          <ListGroup defaultActiveKey="#link1">
          {locations.map((location) => (

            <ListGroup.Item variant="light" action href="#link1">
              {location.name} <Badge bg="success">2</Badge>
            </ListGroup.Item>
  
          ))}
          </ListGroup>
          </div>
          
            <div>
              <h5>Patients</h5>
              <ListGroup defaultActiveKey="#link1">
                  <ListGroup.Item variant="light" action href="#link1">
                    John Gotti<Badge bg="success">2</Badge>
                  </ListGroup.Item>
                  <ListGroup.Item action href="#link2">
                    This one is a button
                  </ListGroup.Item>
            </ListGroup>
          </div>
    </Stack>
    );
  }
