import Body from '../components/Body';
import Messages from '../components/MessageComponents/Messages';
import SideBar from '../components/Sidebar';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function MessagesPage(){

    return(
        <Body>
            <Container>
            <Row>
                <Col sm={2}><SideBar/></Col>
                <Col><Messages/></Col>
            </Row>
            </Container>
        </Body>
    );
}