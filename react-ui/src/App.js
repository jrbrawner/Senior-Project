import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import ProvidersPage from './pages/ProvidersPage';
import OfficesPage from './pages/OfficesPage'
import OfficePage from './pages/OfficePage'


export default function App(){

  return (
    
      <Container fluid className="App">
        <BrowserRouter>
        <Header/>
          <Routes>
            <Route path="/provider" element={<ProvidersPage/>}/>
            <Route path="/office" element={<OfficesPage/>}/>
            <Route path="/office/:officeId" element={<OfficePage />} />
          </Routes>
        </BrowserRouter>
      </Container>
  );
}