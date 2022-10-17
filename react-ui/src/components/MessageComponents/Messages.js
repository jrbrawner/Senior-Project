import React from 'react';
import { useNavigate } from 'react-router-dom';
import MessageDataService from '../../services/message.service';

export default function App(){

    const [messages, setMessages] = React.useState(0);
    const [users, setUsers ] = React.useState(0);
    var arr = [];
    const navigate = useNavigate();

    React.useEffect(() => {
        MessageDataService.getAll().then((response) => {
            setMessages(response.data);
        
            Object.keys(response.data).map((e) => {
                console.log(e, i.sender_id);
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
      {messages.map((message) => (
        <ul key={message.id}>
          <li>Sender ID{message.sender_id}</li>
          <li>Recipient ID {message.recipient_id}</li>
          <li>Body {message.body}</li>
          <li>Timestamp {message.timestamp}</li>
        </ul>
        
      ))}
    </div>
    );
}