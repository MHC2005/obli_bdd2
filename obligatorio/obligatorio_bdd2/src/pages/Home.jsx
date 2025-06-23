import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';
import './Home.css';

function Home() {
  const { user, logout } = useUser();
  const navigate = useNavigate();

  const getRoleIcon = (role) => {
    return role === 'presidente' ? '👑' : '🗳️';
  };

  const getRoleText = (role) => {
    return role === 'presidente' ? 'Presidente de Mesa' : 'Votante';
  };

  return (
    <div className="home-container">
      <div className="home-content">
        <div className="home-icon">
          {getRoleIcon(user.rol)}
        </div>
        <h2 className="home-welcome">
          Bienvenido, {user.ci}
          <span className="role-badge">{getRoleText(user.rol)}</span>
        </h2>
        
        <div className="home-buttons">
          {user.rol === 'votante' && (
            <button 
              className="home-button vote" 
              onClick={() => navigate('/votar')}
            >
              Ir a Votar
            </button>
          )}
          
          {user.rol === 'presidente' && (
            <>
              <button 
                className="home-button president" 
                onClick={() => navigate('/autorizar')}
              >
                Autorizar Voto Observado
              </button>
              <button 
                className="home-button president" 
                onClick={() => navigate('/cerrar-mesa')}
              >
                Cerrar Mesa
              </button>
            </>
          )}
        </div>
        
        <button 
          className="home-button logout" 
          onClick={() => { logout(); navigate('/login'); }}
        >
          Cerrar Sesión
        </button>
      </div>
    </div>
  );
}

export default Home;
