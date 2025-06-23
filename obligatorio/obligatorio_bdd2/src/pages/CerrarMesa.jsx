import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './CerrarMesa.css';

function CerrarMesa() {
  const navigate = useNavigate();
  const [isClosing, setIsClosing] = useState(false);

  const handleCerrar = () => {
    setIsClosing(true);
    
    // Simulación de proceso de cierre
    setTimeout(() => {
      // En el futuro: petición al backend
      alert('Mesa cerrada exitosamente. No se permiten más votos.');
      setIsClosing(false);
      navigate('/home');
    }, 2000);
  };

  const handleCancel = () => {
    navigate('/home');
  };

  return (
    <div className="cerrar-mesa-container">
      <div className="cerrar-mesa-content">
        <div className="cerrar-mesa-icon">
          🔒
        </div>
        <h2 className="cerrar-mesa-title">Cerrar Mesa de Votación</h2>
        
        <div className="warning-message">
          <strong>¡Atención!</strong> Esta acción cerrará permanentemente la mesa de votación. 
          Una vez cerrada, no se permitirán más votos y el proceso será irreversible.
        </div>

        <div className="info-section">
          <div className="info-title">Información del Cierre:</div>
          <div className="info-text">
            • Se finalizará el período de votación<br/>
            • Se generarán los reportes finales<br/>
            • Se bloquearán nuevos accesos al sistema<br/>
            • Los resultados quedarán registrados permanentemente
          </div>
        </div>

        <div className="cerrar-mesa-buttons">
          <button 
            className="cerrar-mesa-button" 
            onClick={handleCerrar}
            disabled={isClosing}
          >
            {isClosing ? 'Cerrando Mesa...' : 'Confirmar Cierre de Mesa'}
          </button>
          
          <button 
            className="cerrar-mesa-button cancel-button" 
            onClick={handleCancel}
            disabled={isClosing}
          >
            Cancelar y Volver
          </button>
        </div>
      </div>
    </div>
  );
}

export default CerrarMesa;
