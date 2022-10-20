import React from 'react';
import { useNavigate } from 'react-router-dom';
import MessageDataService from '../../services/message.service';
import Form from 'react-bootstrap/Form';
import Stack from 'react-bootstrap/Stack';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import MessageSidebar from '../MessageSidebar';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function App(){

    const [messages, setMessages] = React.useState(0);
    const [locations, setLocations] = React.useState(0);
    const [users, setUsers ] = React.useState(0);
    const [currentUser, setCurrentUser] = React.useState(0);
    
    const navigate = useNavigate();

    React.useEffect(() => {
      MessageDataService.getLocations().then((response) => {
          setLocations(response.data);
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
            }
            });
      
      }, []);

    const selectedUserMessages = (userId) => {

      MessageDataService.getUserMessages(userId).then((response) => {
      setMessages(response.data);
      setCurrentUser(userId);
          
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
        }
        });
    }

    const loadPeople = (id) => {

      MessageDataService.getUsers(id).then((response) => {
      setUsers(response.data);
        
      var firstLocationId = locations[0].name;
  
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
      }
      });
    }

    const sendMessage = e => {
        
      e.preventDefault();
      const formData = new FormData(e.target);
      console.log(currentUser);
      console.log("Message sent")
      
      MessageDataService.sendMessage(currentUser, formData).then((response) => {

        document.getElementById("msgBox").value = "";

    
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
        }
        });

    }
    
        

    if (!messages && !locations) return <p>Loading</p>

    if (!messages) return(
        <Container>
          <Row>
            <Col sm={2}>
              <MessageSidebar locations={locations} selectedUserMessages={selectedUserMessages} loadPeople={loadPeople} users={users} />
            </Col>
          </Row>
        </Container>
      ); 

    return(
      <div>
        <Container>
          <Row>
            
            <Col sm={2}>
              <MessageSidebar locations={locations} selectedUserMessages={selectedUserMessages} loadPeople={loadPeople} users={users} />
              </Col>
            
            <Col>
            
              <Stack gap={2} style={{ height: '700px', overflowY: 'auto', width:'' }}>
              

                {messages.map((message) => {
                  
                if(message.sender_id != null ){
                    return (
                      <Card
                      key={message.id}
                      style={{ width: '25%' }}
                      className="ms-5"
                      bg="primary"
                      text="white">
                      <Card.Header>
                        {message.sender_id}
                        <small className="float-end" >{message.timestamp}</small>
                      </Card.Header>
                      <ListGroup variant="flush">
                        <ListGroup.Item>{message.body}</ListGroup.Item>
                      </ListGroup>
                    </Card>
                    )}
                    
                    else{
                      
                      return (
                        <Card
                        key={message.id}
                        style={{ width: '25%' }}
                        className="ms-auto me-5"
                        bg="success"
                        text="white">
                    <Card.Header>
                      {message.sender_id}
                      <small className="float-end" >{message.timestamp}</small>
                    </Card.Header>
                    <ListGroup variant="flush">
                      <ListGroup.Item>{message.body}</ListGroup.Item>
                    </ListGroup>
                  </Card>
                  )}
                  
                })}
  
                
              
              </Stack>
              
              

                <Form onSubmit={sendMessage}>
                  <Row>
                    <Col xs={9}>
                    <Form.Group className="mt-2">
                      <Form.Control required type="text" id="msgBox" name="msg" placeholder="Insert message..." />
                    </Form.Group>
                    </Col>

                  <Col>
                  <div className="mt-2">
                    <Button variant="outline-success" type="submit">Send Message</Button>
                    <div className="vr" />
                    <Button variant="outline-danger">Clear</Button>
                  </div>
                  </Col>
                  </Row>

                </Form>
                
              

              </Col>  

            </Row>
          </Container>
        </div>
        
    
    )
    
    
}