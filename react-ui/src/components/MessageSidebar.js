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
  const handlePageClick = props.handlePageClick;
  const itemOffset = props.itemOffset;
  var currentItems = props.currentItems;

  
  //React.useEffect(() => {
    // Fetch items from another resources.
    //const endOffset = itemOffset + itemsPerPage;
    //console.log(`Loading items from ${itemOffset} to ${endOffset}`);
    
    //if ((Array.isArray(users))){
    //  currentItems = users.slice(itemOffset, endOffset)
    //  console.log(pageCount);
    //}
    //}
    //console.log(pageCount);
    //setCurrentItems(users.slice(itemOffset, endOffset));
    //setCurrentItems(Array.isArray(users) ? users.slice(itemOffset, endOffset) : []);
    //setPageCount(Math.ceil(users.length / itemsPerPage));

  //}, [itemOffset, itemsPerPage]);

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
        pageRangeDisplayed={2}
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
  