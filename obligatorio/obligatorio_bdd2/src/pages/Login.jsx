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
        login({
          ci: data.ci,
          rol: data.rol,
          nombre_completo: data.nombre_completo,
          id_circuito: data.id_circuito,
          barrio: data.barrio,
          departamento: data.departamento
        });

        // Redirigir según el rol del usuario
        if (data.rol === 'presidente') {
          console.log('Presidente detectado, redirigiendo a administración');
          navigate('/admin');
        } else {
          console.log('Votante detectado, redirigiendo a votar');
          navigate('/votar');
        }
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
          <p><strong>Acceso al Sistema:</strong></p>
          <p>• <strong>Presidente:</strong> CI <code>11111111</code> → Panel de Administración</p>
          <p>• <strong>Votantes:</strong> Cualquier otra CI (ej: <code>22222222</code>) → Sistema de Votación</p>
          <p><small>Contraseña para todos: <code>password</code></small></p>
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
