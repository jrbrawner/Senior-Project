import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import OrganizationsPage from './pages/OrganizationsPage';
import LocationsPage from './pages/LocationsPage'
import LocationPage from './pages/LocationPage'
import UsersPage from './pages/UserPage';
import EditUserPage from './pages/EditUserPage';
import LoginPage from './pages/LoginPage';

export default function App(){

  return (
    
      <Container fluid className="App">
        <BrowserRouter>
        <Header/>
          <Routes>
            <Route path="/login" element={<LoginPage/>}/>
            <Route path="/logout"/>

            <Route path="/organization" element={<OrganizationsPage/>}/>
            
            <Route path="/location" element={<LocationsPage/>}/>
            <Route path="/location/:locationId" element={<LocationPage />} />
            
            <Route path="/user" element={<UsersPage />} />
            <Route path="/user/:userId" element={<EditUserPage/>} />

          </Routes>
        </BrowserRouter>
      </Container>
  );
}