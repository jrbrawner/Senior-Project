import React, { Component } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import Pager from "../PagingComponents/Pager";

const generateData = (quantity = 5) => {
  return Array.from({ length: quantity }, (value, index) => ({
    id: index,
    name: `Item name ${index}`,
    price: 2100 + index,
    date: `August 29th 2018`,
    phone: `1-800-111-1117`
  }));
};

const columns = [
  {
    dataField: "id",
    text: "ID",
    sort: true
  },
  {
    dataField: "name",
    text: "Name",
    sort: true
  },
  {
    dataField: "price",
    text: "Price",
    sort: true
  },
  {
    dataField: "date",
    text: "Date",
    sort: true
  },
  {
    dataField: "phone",
    text: "Phone",
    sort: true
  }
];

export default class Notifications extends Component {
  render() {
    return (
      <div className="App">
        <h1>Hello CodeSandbox</h1>
        <h2>Start editing to see some magic happen!</h2>
        <Pager
          items={generateData(20)}
          itemsPerPage={5}
          top
          render={(items) => (
            <BootstrapTable
              keyField="id"
              data={items}
              columns={columns}
              condensed
              striped
              hover
              bordered={false}
            />
          )}
        />
      </div>
    );
  }
}


