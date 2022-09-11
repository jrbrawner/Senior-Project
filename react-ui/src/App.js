import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import ProvidersPage from './pages/ProvidersPage';
import OfficesPage from './pages/OfficesPage'


export default function App(){

  return (
    
      <Container fluid className="App">
        <BrowserRouter>
        <Header/>
          <Routes>
            <Route path="/provider" element={<ProvidersPage/>}/>
            <Route path="/office" element={<OfficesPage/>}/>
          </Routes>
        </BrowserRouter>
      </Container>
  );
}