import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';

function Login() {
  const navigate = useNavigate();
  const { login } = useUser();

  const handleSubmit = (e) => {
    e.preventDefault();
    const ci = e.target.ci.value;
    const cc = e.target.cc.value;

    // Simulación de rol (usar fetch al backend después)
    const rol = ci === '11111111' ? 'presidente' : 'votante';

    login({ ci, cc, rol });
    navigate('/home');
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Iniciar sesión</h2>
      <input name="ci" type="text" placeholder="Cédula" required />
      <input name="cc" type="text" placeholder="Credencial Cívica" required />
      <button type="submit">Ingresar</button>
    </form>
  );
}

export default Login;
