import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './Votar.css';

function Votar() {
  const navigate = useNavigate();
  const [selectedOption, setSelectedOption] = useState('');
  const [isVoting, setIsVoting] = useState(false);

  const handleVote = (e) => {
    e.preventDefault();
    if (!selectedOption) {
      alert('Por favor seleccione una opción antes de votar.');
      return;
    }

    setIsVoting(true);
    
    // Simulación de proceso de votación
    setTimeout(() => {
      // En el futuro: enviar voto al backend con fetch
      alert('¡Voto emitido con éxito! Gracias por participar en el proceso democrático.');
      setIsVoting(false);
      navigate('/home');
    }, 2000);
  };

  const handleSelectChange = (e) => {
    setSelectedOption(e.target.value);
  };

  const handleVolver = () => {
    navigate('/home');
  };

  return (
    <div className="votar-container">
      <div className="votar-content">
        <div className="votar-icon">
          🗳️
        </div>
        <h2 className="votar-title">Emitir Voto</h2>
        
        <div className="votar-instructions">
          <strong>Instrucciones:</strong> Seleccione cuidadosamente la lista de su preferencia. 
          Una vez confirmado su voto, no podrá modificarlo.
        </div>

        <form className="votar-form" onSubmit={handleVote}>
          <div className="select-group">
            <label className="select-label" htmlFor="lista-select">
              📋 Seleccione una Lista Electoral:
            </label>
            <select 
              id="lista-select"
              className="votar-select"
              value={selectedOption}
              onChange={handleSelectChange}
              required
              disabled={isVoting}
            >
              <option value="">-- Seleccione una lista --</option>
              <option value="1" className="option-partido-a">
                🔵 Lista 1 - Partido Democrático
              </option>
              <option value="2" className="option-partido-b">
                🔴 Lista 2 - Partido Nacional
              </option>
              <option value="3">
                🟢 Lista 3 - Frente Amplio
              </option>
              <option value="4">
                🟡 Lista 4 - Partido Independiente
              </option>
            </select>
          </div>

          <button 
            className="votar-button" 
            type="submit"
            disabled={isVoting || !selectedOption}
          >
            {isVoting ? '⏳ Procesando Voto...' : 'Confirmar Voto'}
          </button>
        </form>

        <div className="security-notice">
          Su voto es secreto y será registrado de forma segura en el sistema.
        </div>

        <div className="votar-nav">
          <button 
            className="nav-button" 
            onClick={handleVolver}
            disabled={isVoting}
          >
            Volver al Inicio
          </button>
        </div>
      </div>
    </div>
  );
}

export default Votar;
