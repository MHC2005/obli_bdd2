import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import Votar from './pages/Votar';
import Autorizar from './pages/Autorizar';
import CerrarMesa from './pages/CerrarMesa';
import Admin from './pages/Admin';
import Personas from './components/Personas';
import { useUser } from './context/UserContext';

function App() {
  const { user, loading } = useUser();

  if (loading) return <div>Cargando sesión...</div>; // <-- evitar render hasta que esté listo

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/home" element={user ? <Home /> : <Navigate to="/login" />} />
      <Route path="/admin" element={user?.rol === 'presidente' ? <Admin /> : <Navigate to="/login" />} />
      <Route path="/votar" element={user?.rol === 'votante' ? <Votar /> : <Navigate to="/login" />} />
      <Route path="/autorizar" element={user?.rol === 'presidente' ? <Autorizar /> : <Navigate to="/login" />} />
      <Route path="/cerrar-mesa" element={user?.rol === 'presidente' ? <CerrarMesa /> : <Navigate to="/login" />} />
      <Route path="/personas" element={user ? <Personas /> : <Navigate to="/login" />} />
    </Routes>
  );
}

export default App;
