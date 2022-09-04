import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import ProviderPage from './pages/ProviderPage';
import LoginPage from './pages/LoginPage';
import PhysicianPage from './pages/PhysicianPage';

export default function App(){

  return (
    
      <Container fluid className="App">
        <BrowserRouter>
        <Header/>
          <Routes>
            <Route path="/provider" element={<ProviderPage/>}/>
            <Route path="/login" element={<LoginPage/>}/>
            <Route path='/physician/:id' element={<PhysicianPage/>}/>
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </BrowserRouter>
      </Container>
  );
}