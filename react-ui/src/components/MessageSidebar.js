import React from "react";
import { Button, Badge, ListGroup, Stack } from "react-bootstrap";
import MessageDataService from '../services/message.service';
import { useNavigate } from 'react-router-dom';
import paginationFactory from "react-bootstrap-table2-paginator";
import BootstrapTable from "react-bootstrap-table-next";

export default function Sidebar(props) {

  
  const navigate = useNavigate();

  const locations = props.locations;
  const selectedUserMessages = props.selectedUserMessages;
  const users = props.users;
  const loadPeople = props.loadPeople;
  const selectedRow = null;
  
  const rowEvents = {
    onClick: (e, row, rowIndex) => {
      selectedUserMessages(row.id);
      
    }
  };

  const columns = [
    {
      dataField: "name",
      text: "User Name",
      isDummyField: true,
      headerAttrs: {
        hidden: true
      },
      formatter: (cellContent, row, index, extraData) => {
        return(
        <td key={row.id}>
          {row.name}<Badge bg="success">{row.unread_msg}</Badge>
        </td> 
        
        )
      }
    }
  ]
    //if (locations.length === 1){

      //var firstLocationId = locations[0].id;
      //loadPeople(firstLocationId);

    //}

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

      <BootstrapTable
      bootstrap4
      keyField="id"
      data={users}
      columns={columns}
      rowEvents={ rowEvents }
      wrapperClasses="responsive"
      hover
      selectRow={{
        mode: "radio",
        hideSelectColumn: true,
        clickToSelect: true,
        bgColor: "#99ccff",
      }}
      pagination={paginationFactory({ sizePerPage: 13 })}
      />
        

    </Stack>
    )
}
  