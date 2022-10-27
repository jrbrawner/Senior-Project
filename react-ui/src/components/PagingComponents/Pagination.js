import React, { Component } from "react";
import PropTypes from "prop-types";
import { Pagination as BsPagination } from "react-bootstrap";
import classnames from "classnames";

class Pagination extends Component {
  handleOnSelect = page => this.props.onPageClick(page);

  handleViewAllPages = e => {
    e.preventDefault();
    this.handleOnSelect(0);
  };

  render() {
    const { numberOfPages, maxButtons, activePage, viewAll } = this.props;

    if (numberOfPages <= 1) return null;

    const viewAllClassName = classnames({
      active: !activePage
    });

    return (
      <div>
        <BsPagination
          activePage={activePage}
          items={numberOfPages}
          maxButtons={maxButtons}
          first
          last
          next
          prev
          onSelect={this.handleOnSelect}
        />
        {viewAll && (
          <ul className="pagination pagination__view-all-button">
            <li className={viewAllClassName}>
              {
                // Using link instead of button because we're leveraging
                // Bootstrap pagination css
                //eslint-disable-next-line
                <a role="button" href="#" onClick={this.handleViewAllPages}>
                  View All
                </a>
              }
            </li>
          </ul>
        )}
      </div>
    );
  }
}

Pagination.propTypes = {
  numberOfPages: PropTypes.number.isRequired,
  activePage: PropTypes.number,
  onPageClick: PropTypes.func.isRequired,
  viewAll: PropTypes.bool,
  /** The maximum number of page buttons visible at a given time */
  maxButtons: PropTypes.number
};

Pagination.defaultProps = {
  maxButtons: 10
};

export default Pagination;
