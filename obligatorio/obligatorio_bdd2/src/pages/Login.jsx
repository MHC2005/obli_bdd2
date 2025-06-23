import { useUser } from '../context/UserContext';
import './Login.css';
import { useNavigate } from 'react-router-dom';

function Login() {
  const { login } = useUser();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const ci = e.target.ci.value;
    const cc = e.target.cc.value;

    // Simulación de roles (usar fetch al backend después)
    let rol = 'votante'; // Por defecto todos son votantes

    if (ci === '11111111') {
      rol = 'presidente';
    }

    login({ ci, cc, rol });
    navigate('/home');
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="login-icon">
          🗳️
        </div>
        <h2 className="login-title">Sistema de Votación</h2>

        <div className="login-info">
          <p><strong>Usuarios de prueba:</strong></p>
          <p>• Presidente: CI <code>11111111</code></p>
          <p>• Votante: Cualquier otra CI (ej: <code>22222222</code>)</p>
        </div>

        <div className="input-group">
          <input 
            className="login-input"
            name="ci" 
            type="text" 
            placeholder="Cédula de Identidad" 
            required 
          />
        </div>
        <div className="input-group">
          <input 
            className="login-input"
            name="cc" 
            type="text" 
            placeholder="Credencial Cívica" 
            required 
          />
        </div>
        <button className="login-button" type="submit">
          Ingresar al Sistema
        </button>
      </form>
    </div>
  );
}

export default Login;
