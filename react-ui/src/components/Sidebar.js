import React from "react";
import { Button, Badge, ListGroup, Stack } from "react-bootstrap";

export default function Sidebar() {

  const alertClicked = () => {
    alert('You clicked the third ListGroupItem');
  };

   
    return (
      <Stack gap={3}>
            <div className="dfdf">
              <h5>Locations</h5>
              <ListGroup defaultActiveKey="#link1">
                  <ListGroup.Item variant="light" action href="#link1">
                    Location 1<Badge bg="success">2</Badge>
                  </ListGroup.Item>
                  <ListGroup.Item action href="#link2">
                    Location 2
                  </ListGroup.Item>
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
