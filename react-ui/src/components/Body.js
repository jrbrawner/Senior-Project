import Container from 'react-bootstrap/Container';
import Stack from 'react-bootstrap/Stack';
import NavigationBar from './NavigationBar';


export default function Body({ NavigationBar, children }) {
  return (
    <Container>
      <Stack direction="horizontal" className="Body">
        {NavigationBar && <NavigationBar />}
        <Container className="Content">
          {children}
        </Container>
      </Stack>
    </Container>
  );
}