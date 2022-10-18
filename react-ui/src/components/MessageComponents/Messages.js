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
    const [people, setPeople] = React.useState(0);
    
    const navigate = useNavigate();


    React.useEffect(() => {

        MessageDataService.getAll().then((response) => {
            setMessages(response.data);
            }).catch(error => {
            if (error.response.status === 401)
            {
                navigate(`/login`);
                console.log('Not authenticated.');
            }
            if (error.response.status === 403)
            {
                alert('You are not authenticated for this page.');
            }
            });
        
        }, []);
    
        React.useEffect(() => {
          MessageDataService.getLocations().then((response) => {
              setLocations(response.data);
              }).catch(error => {
              if (error.response.status === 401)
              {
                  navigate(`/login`);
                  console.log('Not authenticated.');
              }
              if (error.response.status === 403)
              {
                  alert('You are not authenticated for this page.');
              }
              });
          
          }, []);


    if (!messages && !locations) return <p>No data.</p>

    return(
      <div>
        <Container>
          <Row>
            
            <Col sm={2}>
              <MessageSidebar locations={locations}/>
              </Col>
            
            <Col>
            
              <Stack style={{ height: '700px', overflowY: 'auto' }}>

                {messages.map((message) => {
                  if (message.sender_id === 7){
                    return (<Card
                      key={message.id}
                      style={{ width: '30%'}}
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
                  )
                }
                return (
                  <Card
                  key={message.id}
                  style={{ width: '30%' }}
                  className="float-end"
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
                )
              })}
              
              </Stack>
              
              <Stack direction="horizontal" gap={3}>
                <Form.Control className="me-auto" placeholder="Insert message..." />
                <Button variant="outline-success">Send Message</Button>
                <div className="vr" />
                <Button variant="outline-danger">Clear</Button>
              </Stack>
              </Col>

            </Row>
          </Container>
        
      </div>
    
    );
}