import React from "react";
import { Button, Badge, ListGroup, Stack } from "react-bootstrap";
import MessageDataService from '../services/message.service';
import { useNavigate } from 'react-router-dom';
import ReactPaginate from 'react-paginate';

export default function Sidebar(props) {

  const navigate = useNavigate();

  const locations = props.locations;
  const selectedUserMessages = props.selectedUserMessages;
  const users = props.users;
  const loadPeople = props.loadPeople;
  const itemsPerPage = props.itemsPerPage;
  const pageCount = props.pageCount;
  //const currentItems = props.currentItems;

  // We start with an empty list of items.
  const [currentItems, setCurrentItems] = React.useState(null);
  // Here we use item offsets; we could also use page offsets
  // following the API or data you're working with.
  const [itemOffset, setItemOffset] = React.useState(0);


  const handlePageClick = (event) => {
    const newOffset = event.selected * itemsPerPage % users.length;
    console.log(`User requested page number ${event.selected}, which is offset ${newOffset}`);
    setItemOffset(newOffset);
  };

  React.useEffect(() => {
    // Fetch items from another resources.
    const endOffset = itemOffset + itemsPerPage;
    console.log(`Loading items from ${itemOffset} to ${endOffset}`);
    
    
    if ((Array.isArray(users))){
      setCurrentItems(users.slice(itemOffset, endOffset));
      console.log(pageCount);
    }
    console.log(pageCount);
    //setCurrentItems(users.slice(itemOffset, endOffset));
    //setCurrentItems(Array.isArray(users) ? users.slice(itemOffset, endOffset) : []);
    //setPageCount(Math.ceil(users.length / itemsPerPage));

  }, [itemOffset, itemsPerPage]);

  function UsersNoMsg({ currentUsers }) {
    return (
      <div className="items">
      {currentUsers && currentUsers.map((user) => (

        <ListGroup.Item key={user.id} action onClick={() => selectedUserMessages(user.id)} href={`#${user.id}`}>
          {user.name}
        </ListGroup.Item>
      ))}
        </div>
    );
  }

  function UsersMsg({ currentUsers }) {
    return (
      <div className="items">
      {currentUsers && currentUsers.map((user) => (

            <ListGroup.Item key={user.id} action onClick={() => selectedUserMessages(user.id)} href={`#${user.id}`}>
              {user.name} <Badge bg="success">{user.unread_msg}</Badge>
            </ListGroup.Item>
      ))}
        </div>
    );
  }

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

        <UsersNoMsg currentUsers={currentItems}/>
        
      </ListGroup>

      <ReactPaginate
        nextLabel=">"
        onPageChange={handlePageClick}
        pageRangeDisplayed={1}
        marginPagesDisplayed={1}
        pageCount={pageCount}
        initialPage={0}
        previousLabel="<"
        pageClassName="page-item"
        pageLinkClassName="page-link"
        previousClassName="page-item"
        previousLinkClassName="page-link"
        nextClassName="page-item"
        nextLinkClassName="page-link"
        breakLabel="..."
        breakClassName="page-item"
        breakLinkClassName="page-link"
        containerClassName="pagination"
        activeClassName="active"
        />



    </Stack>
    )
}
  