import React from 'react';
import { useNavigate } from 'react-router-dom';
import MessageDataService from '../../services/message.service';
import Toast from 'react-bootstrap/Toast';
import ToastContainer from 'react-bootstrap/ToastContainer';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';


export default function App(){

    const [messages, setMessages] = React.useState(0);
    const [users, setUsers ] = React.useState(0);
    var arr = [];
    const navigate = useNavigate();


    React.useEffect(() => {
        MessageDataService.getAll().then((response) => {
            setMessages(response.data);
        
            Object.keys(response.data).map((e) => {
                console.log(e.sender_id);
              })

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


    if (!messages) return <p>No data.</p>

    return(
      <div>
          <div>
            {messages.map((message) => (
              <ul key={message.id}>
                <li>Sender ID{message.sender_id}</li>
                <li>Recipient ID {message.recipient_id}</li>
                <li>Body {message.body}</li>
                <li>Timestamp {message.timestamp}</li>
              </ul>
          ))}
          </div>
          <Container>
              <Row>
                <Col sm={4}>
                  Stuff over
                </Col>
                <Col sm={8}>
                        <ToastContainer className="p-3">
                        <Toast>
                          <Toast.Header closeButton={false}>
                            <strong className="me-auto">Bootstrap</strong>
                            <small>11 mins ago</small>
                          </Toast.Header>
                          <Toast.Body>
                            Hello, world! This is a toast message.
                            </Toast.Body>
                        </Toast>
                      </ToastContainer>
                </Col>
              </Row>
          </Container>
            
    </div>
        
    
    );
}