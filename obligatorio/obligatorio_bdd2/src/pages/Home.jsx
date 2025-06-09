import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';

function Home() {
  const { user, logout } = useUser();
  const navigate = useNavigate();

  return (
    <div>
      <h2>Hola, {user.ci} ({user.rol})</h2>
      {user.rol === 'votante' && (
        <button onClick={() => navigate('/votar')}>Ir a Votar</button>
      )}
      {user.rol === 'presidente' && (
        <>
          <button onClick={() => navigate('/autorizar')}>Autorizar Voto Observado</button>
          <button onClick={() => navigate('/cerrar-mesa')}>Cerrar Mesa</button>
        </>
      )}
      <br />
      <button onClick={() => { logout(); navigate('/login'); }}>Cerrar Sesión</button>
    </div>
  );
}

export default Home;
