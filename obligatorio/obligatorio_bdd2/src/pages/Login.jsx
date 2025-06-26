import { useUser } from '../context/UserContext';
import './Login.css';
import { useNavigate } from 'react-router-dom';

function Login() {
  const { login } = useUser();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const ci = e.target.ci.value;
    const password = e.target.password.value;

    try {
      const res = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ci, password })
      });

      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.token); 
        login({ ci: data.ci, rol: data.rol });      
        navigate('/home');
      } else {
        alert("Credenciales inválidas");
      }
    } catch (err) {
      alert("Error de conexión");
      console.error(err);
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="login-icon">🗳️</div>
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
            name="password" 
            type="password" 
            placeholder="Contraseña" 
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
