import React, { Component } from "react";
import PropTypes from "prop-types";
import Pagination from "./Pagination";

// TODO - Move into a shared library
/**
 * Borrowed from https://github.com/you-dont-need/You-Dont-Need-Lodash-Underscore#_chunk
 * @param {number} size - The desired size for each chunk
 * @param {Array} input - The array to chunk
 * @returns {Array.<Array>} 2-dimensional array (array of arrays) chunked by size
 */
const chunkBy = (size, input) => {
  return input.reduce(
    // arr = accumulator, item = current item, index = current index
    (arr, item, index) => {
      return index % size === 0
        ? // index matches desired chunk size so
          // copy current accumulator array via spread operator
          // and append a new array containing current item to end
          [...arr, [item]]
        : // index is less than desired chunk size so
          // copy current accumulator array minus last nested array
          // replace last nested array with a new one that has current item appended in it.
          // spread and slice operators are used to flatten every nested array during each reduction step
          [...arr.slice(0, -1), [...arr.slice(-1)[0], item]];
    },
    // initial accumulator value
    []
  );
};

/*
 * TODO: I can't decide if I think that the component names should be
 *        swapped between Pager and Pagination.
 * TODO: Need to do validation of initialPage value passed in?
 */
class Pager extends Component {
  state = { selectedPage: this.props.initialPage };

  calculateTotalPages = () => {
    const { items, itemsPerPage } = this.props;
    return items ? Math.ceil(items.length / itemsPerPage) : 0;
  };

  getCurrentPageOfItems = () => {
    const { items, itemsPerPage } = this.props;
    const { selectedPage } = this.state;

    if (!selectedPage) {
      return items;
    }

    return (
      items && items.length && chunkBy(itemsPerPage, items)[selectedPage - 1]
    );
  };

  handleOnPageClick = selectedPage => {
    if (
      this.state.selectedPage < 0 ||
      this.state.selectedPage === selectedPage
    ) {
      return;
    }

    this.setState({ selectedPage }, () =>
      window.scrollTo({ top: this.wrapper.offsetTop, behavior: "smooth" })
    );
  };

  render() {
    const { top, render } = this.props;
    const { selectedPage } = this.state;
    const totalPages = this.calculateTotalPages();
    const currentPageOfItems = this.getCurrentPageOfItems();

    return (
      // eslint-disable-next-line react/jsx-no-bind
      <div ref={el => (this.wrapper = el)}>
        {top && (
          <Pagination
            numberOfPages={totalPages}
            activePage={selectedPage}
            onPageClick={this.handleOnPageClick}
            viewAll
          />
        )}
        {render(currentPageOfItems)}
        <Pagination
          numberOfPages={totalPages}
          activePage={selectedPage}
          onPageClick={this.handleOnPageClick}
          viewAll
        />
      </div>
    );
  }
}

Pager.propTypes = {
  /** list of data items to page */
  items: PropTypes.array.isRequired,
  /** number of items to show per page */
  itemsPerPage: PropTypes.number.isRequired,
  /** initial page selection */
  initialPage: PropTypes.number,
  /** include pagination controls on top */
  top: PropTypes.bool,
  /** render prop to control display of paged data */
  render: PropTypes.func.isRequired
};

Pager.defaultProps = {
  initialPage: 1,
  top: false
};

export default Pager;
