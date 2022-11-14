import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';


export default function DialogModal(props) {
  const [show, setShow] = useState(false);

  const handleShow = () => setShow(true);
  const handleCloseNoSuccess = () => {
    setShow(false);
  }

  const handleClose = () => {
    setShow(false);
    onSuccess();
  }

  const buttonName = props.buttonName;
  const modalTitle = props.modalTitle;
  const modalBody = props.modalBody;
  const onSuccess = props.onSuccess;

  return (
    <>
      <Button variant="danger" onClick={handleShow}>
        {buttonName}
      </Button>

      <Modal show={show} onHide={handleClose} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{modalTitle}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{modalBody}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseNoSuccess}>
            Close
          </Button>
          <Button variant="danger" onClick={handleClose}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

//render(<DialogModal />);