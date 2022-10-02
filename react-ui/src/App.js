import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import OrganizationsPage from './pages/OrganizationsPage';
import LocationsPage from './pages/LocationsPage'
import LocationPage from './pages/LocationPage'


export default function App(){

  return (
    
      <Container fluid className="App">
        <BrowserRouter>
        <Header/>
          <Routes>
            <Route path="/organization" element={<OrganizationsPage/>}/>
            <Route path="/location" element={<LocationsPage/>}/>
            <Route path="/location/:locationId" element={<LocationPage />} />
          </Routes>
        </BrowserRouter>
      </Container>
  );
}