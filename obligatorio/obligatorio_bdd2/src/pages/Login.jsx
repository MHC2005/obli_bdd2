import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';

function Login() {
  const { login } = useUser();
  const navigate = useNavigate();

  const handleLogin = () => {
    // Simulación de login, podrías reemplazarlo por un fetch a una API real
    login({ ci: 12345678, rol: 'presidente' });
    navigate('/home');
  };

  return (
    <div>
      <h2>Login</h2>
      <button onClick={handleLogin}>Iniciar sesión</button>
    </div>
  );
}

export default Login;