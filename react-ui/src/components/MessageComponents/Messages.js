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
import {useEffect, useRef, useState} from 'react';

export default function App(){

    const [messages, setMessages] = React.useState(0);
    const [locations, setLocations] = React.useState(0);
    const [users, setUsers ] = React.useState(0);
    const [currentUser, setCurrentUser] = React.useState(null);
    const [currentLocation, setCurrentLocation] = React.useState(0);
    const bottomRef = useRef(null);
    
    const navigate = useNavigate();

    React.useEffect(() => {
      MessageDataService.getLocations().then((response) => {

          setLocations(response.data);
          //if (locations.length === 1){

            //var firstLocationId = locations[0].id;
            //loadPeople(firstLocationId);

          //}
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
                if (error.response.status === 500){
                  navigate(`/login`);
                  console.log('Not authenticated.');
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
      setCurrentLocation(id);
      
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
      console.log(currentLocation);
      
      MessageDataService.sendMessage(currentUser, currentLocation, formData).then((response) => {

        document.getElementById("msgBox").value = "";
        MessageDataService.getUserMessages(currentUser);

    
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

      function ClearTextBox() {
        document.getElementById("msgBox").value = "";

      }

      function openPicture(photoId) {
        MessageDataService.loadPicture(photoId).then((response) => {
          console.log(response.data)
        }
        );
      }

      //const loadPhoto = e => {
      //  e.preventDefault;
//
  //      MessageDataService.loadPicture(e)
    //  }

      useEffect(() => {
        // 👇️ scroll to bottom every time messages change
        bottomRef.current?.scrollIntoView();
      }, [messages]);

      setTimeout(() => {
        if (currentUser !== null){
            console.log('Refreshing Messages...')
          MessageDataService.getUserMessages(currentUser).then((response) => {
            setMessages(response.data);
            setCurrentUser(currentUser);
              
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
      }, 10000);

      
    
        

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
                //users messages
                if(message.sender_id != null){
                    return (
                      <Card
                      key={message.id}
                      style={{ width: '16rem' }}
                      className="ms-5"
                      bg="primary"
                      text="white">
                      <Card.Header>
                        {message.sender_name}
                        <small className="float-end" >{message.timestamp}</small>
                      </Card.Header>
                      <ListGroup variant="flush">
                        <ListGroup.Item>
                        {message.photos.map((photo) => {
                        return (<a target="_blank" href={`/api/load-photo/${photo.photo}`}>Photo </a>)
                        })
                      }
                          <Card.Text>{message.body}</Card.Text>
                          </ListGroup.Item>
                      </ListGroup>
                    </Card>
                    
                    )}
                    
                    
                    else{
                      
                      return (
                        //orgs messages
                        <Card
                        key={message.id}
                        style={{ width: '16rem' }}
                        className="ms-auto me-5"
                        bg="success"
                        text="white">
                    <Card.Header>
                      {message.sender_id}
                      <small className="float-end" >{message.timestamp}</small>
                    </Card.Header>
                    <ListGroup variant="flush">
                      <ListGroup.Item>
                      <Card.Text>{message.body}</Card.Text>
                        </ListGroup.Item>
                    </ListGroup>
                  </Card>
                    
                  
                  )}
                  
                })}
  
                  
              <div ref={bottomRef}/>
                
                
              
              </Stack>
              
                <Form onSubmit={sendMessage}>
                  <Row>
                    <Col xs={9}>
                    <Form.Group className="mt-2">
                      <Form.Control required type="text" id="msgBox" name="msg" autoComplete="off" placeholder="Insert message..." />
                    </Form.Group>
                    </Col>

                  <Col>
                  <div className="mt-2">
                    <Button variant="outline-success" type="submit">Send Message</Button>
                    <div className="vr" />
                    <Button variant="outline-danger" onClick={() => ClearTextBox()}>Clear</Button>
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