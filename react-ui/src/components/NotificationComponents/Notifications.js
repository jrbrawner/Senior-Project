import ReactPaginate from "react-paginate";
import React, {
  useEffect,
  useState
} from "react";
import MessageDataService from '../../services/message.service';
import {Stack, ListGroup} from 'react-bootstrap';

const items = [...Array(33).keys()];

function Items({ currentItems }) {
  return (
    <div className="items">
    {currentItems && currentItems.map((item) => (
      <Stack>
        <ListGroup>
          <ListGroup.Item key={item.id} action href={`#${item.id}`}>{item.name}</ListGroup.Item>
        </ListGroup>
      </Stack>
      
    ))}
      </div>
  );
}

export default function Notifications({ itemsPerPage }) {
  // We start with an empty list of items.
  const [currentItems, setCurrentItems] = useState(null);
  const [pageCount, setPageCount] = useState(0);
  // Here we use item offsets; we could also use page offsets
  // following the API or data you're working with.
  const [itemOffset, setItemOffset] = useState(0);
  const [users, setUsers] = useState(null);

  const filterText = "";

  React.useEffect(() => {
    MessageDataService.getUsers(2).then((response) => {
      setUsers(response.data);

      const endOffset = itemOffset + itemsPerPage;
      setCurrentItems(users.slice(itemOffset, endOffset));
      setPageCount(Math.ceil(users.length / itemsPerPage));
      

    }).catch(error => {
    });
  }, [itemOffset, itemsPerPage]);

  // Invoke when user click to request another page.
  const handlePageClick = (event) => {
    const newOffset = event.selected * itemsPerPage % items.length;
    console.log(`User requested page number ${event.selected}, which is offset ${newOffset}`);
    setItemOffset(newOffset);
  };

  const handleFilterTextChange = (event) => {

  }

  
  return (
    <div id="container">
      
      <Items currentItems={currentItems} />
      
      <ReactPaginate
        nextLabel=">"
        onPageChange={handlePageClick}
        pageRangeDisplayed={3}
        marginPagesDisplayed={2}
        pageCount={pageCount}
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
        renderOnZeroPageCount={null}
        />
      </div>
  )
}