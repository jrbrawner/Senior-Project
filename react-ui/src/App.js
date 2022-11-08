import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import {BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import OrganizationsPage from './pages/OrganizationsPage';
import LocationsPage from './pages/LocationsPage'
import LocationPage from './pages/LocationPage'
import UsersPage from './pages/UserPage';
import EditUserPage from './pages/EditUserPage';
import LoginPage from './pages/LoginPage';
import LogoutPage from './pages/LogoutPage';
import NewUserPage from './pages/NewUserPage';
import MessagesPage from './pages/MessagesPage';
import PendingUsersPage from './pages/PendingUsersPage';
import NotificationPage from './pages/NotificationPage';
import LocationAnnouncementPage from './pages/LocationAnnouncementPage';
import RolesPage from './pages/RolesPage';
import RolePage from './pages/RolePage';


export default function App(){

  return (
    
      <Container fluid className="App">
        <BrowserRouter>
        <Header/>
          <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<LoginPage/>}/>
            <Route path="/logout" element={<LogoutPage/>}/>

            <Route path="/organization" element={<OrganizationsPage/>}/>
            
            <Route path="/location" element={<LocationsPage/>}/>
            <Route path="/location/:locationId" element={<LocationPage />} />
            <Route path="/location/:locationId/announcement" element={<LocationAnnouncementPage/>}/>
            
            <Route path="/user" element={<UsersPage />} />
            <Route path="/user/:userId" element={<EditUserPage/>} />
            <Route path="/user/create" element={<NewUserPage/>} />
            <Route path="/user/new" element={<PendingUsersPage/>} />

            <Route path="/messages" element={<MessagesPage/>} />

            <Route path="/notifications" element={<NotificationPage/>} />

            <Route path="/role" element={<RolesPage/>} />
            <Route path="/role/:roleId" element={<RolePage/>} />

          </Routes>
        </BrowserRouter>
      </Container>
  );
}