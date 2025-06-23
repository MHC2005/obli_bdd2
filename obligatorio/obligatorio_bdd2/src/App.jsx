import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import Votar from './pages/Votar';
import Autorizar from './pages/Autorizar';
import CerrarMesa from './pages/CerrarMesa';
import Personas from './components/Personas';
import { useUser } from './context/UserContext';

function App() {
  const { user } = useUser();

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />

      <Route path="/login" element={<Login />} />

      <Route
        path="/home"
        element={user ? <Home /> : <Navigate to="/login" />}
      />

      <Route
        path="/votar"
        element={user?.rol === 'votante' ? <Votar /> : <Navigate to="/home" />}
      />

      <Route
        path="/autorizar"
        element={user?.rol === 'presidente' ? <Autorizar /> : <Navigate to="/home" />}
      />

      <Route
        path="/cerrar-mesa"
        element={user?.rol === 'presidente' ? <CerrarMesa /> : <Navigate to="/home" />}
      />

      <Route
        path="/personas"
        element={user ? <Personas /> : <Navigate to="/login" />}
      />
    </Routes>
  );
}

export default App;
