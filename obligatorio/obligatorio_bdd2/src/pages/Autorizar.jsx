import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './Autorizar.css';

function Autorizar() {
  const navigate = useNavigate();
  
  // Simulación de solicitudes pendientes (más adelante vendrá del backend)
  const [solicitudes, setSolicitudes] = useState([
    {
      id: 1,
      ci: '12345678',
      motivo: 'Dificultad para leer la papeleta debido a problemas de visión',
      fecha: '2025-06-23 14:30',
      estado: 'pendiente'
    },
    {
      id: 2,
      ci: '87654321',
      motivo: 'Solicitud de asistencia por discapacidad motriz',
      fecha: '2025-06-23 15:15',
      estado: 'pendiente'
    },
    {
      id: 3,
      ci: '11223344',
      motivo: 'Consulta sobre candidatos antes de votar',
      fecha: '2025-06-23 15:45',
      estado: 'pendiente'
    }
  ]);

  const handleAprobar = (id) => {
    setSolicitudes(prev => 
      prev.map(sol => 
        sol.id === id ? { ...sol, estado: 'aprobado' } : sol
      )
    );
    alert(`Solicitud ${id} aprobada. El votante puede proceder.`);
  };

  const handleRechazar = (id) => {
    setSolicitudes(prev => 
      prev.map(sol => 
        sol.id === id ? { ...sol, estado: 'rechazado' } : sol
      )
    );
    alert(`Solicitud ${id} rechazada.`);
  };

  const handleVolver = () => {
    navigate('/home');
  };

  const solicitudesPendientes = solicitudes.filter(sol => sol.estado === 'pendiente');

  return (
    <div className="autorizar-container">
      <div className="autorizar-content">
        <div className="autorizar-icon">
          👔
        </div>
        <h2 className="autorizar-title">Autorizar Votos Observados</h2>
        
        {solicitudesPendientes.length > 0 ? (
          <div className="status-message pending">
            <strong>Solicitudes Pendientes:</strong> {solicitudesPendientes.length} 
            {solicitudesPendientes.length === 1 ? ' solicitud requiere' : ' solicitudes requieren'} 
            tu autorización como Presidente de Mesa.
          </div>
        ) : (
          <div className="status-message">
            <strong>¡Todo al día!</strong> No hay solicitudes pendientes de autorización en este momento.
          </div>
        )}

        <div className="solicitudes-container">
          {solicitudesPendientes.length > 0 ? (
            solicitudesPendientes.map((solicitud) => (
              <div key={solicitud.id} className="solicitud-item">
                <div className="solicitud-header">
                  <div className="solicitud-ci">
                    👤 Cédula: {solicitud.ci}
                  </div>
                  <div className="solicitud-estado">
                    {solicitud.estado.toUpperCase()}
                  </div>
                </div>
                
                <div className="solicitud-detalles">
                  <strong>Motivo:</strong> {solicitud.motivo}<br/>
                  <strong>Fecha:</strong> {solicitud.fecha}
                </div>
                
                <div className="solicitud-acciones">
                  <button 
                    className="autorizar-button aprobar"
                    onClick={() => handleAprobar(solicitud.id)}
                  >
                    ✅ Aprobar
                  </button>
                  <button 
                    className="autorizar-button rechazar"
                    onClick={() => handleRechazar(solicitud.id)}
                  >
                    ❌ Rechazar
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="empty-state">
              <div className="empty-state-icon">📝</div>
              <div className="empty-state-text">
                No hay solicitudes pendientes de autorización.
              </div>
            </div>
          )}
        </div>

        <div className="autorizar-nav">
          <button className="nav-button" onClick={handleVolver}>
            Volver al Inicio
          </button>
        </div>
      </div>
    </div>
  );
}

export default Autorizar;
