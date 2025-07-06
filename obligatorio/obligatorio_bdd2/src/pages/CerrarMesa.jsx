import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import './CerrarMesa.css';

function CerrarMesa() {
  const navigate = useNavigate();
  const { user } = useUser();
  const [estadoMesa, setEstadoMesa] = useState(null);
  const [loading, setLoading] = useState(true);
  const [procesando, setProcesando] = useState(false);
  const [motivo, setMotivo] = useState('');

  useEffect(() => {
    // Verificar que el usuario sea presidente
    if (!user || user.rol !== 'presidente') {
      alert('Acceso denegado. Solo el presidente puede gestionar la mesa de votación.');
      navigate('/login');
      return;
    }

    cargarEstadoMesa();
  }, [user, navigate]);

  const cargarEstadoMesa = async () => {
    try {
      setLoading(true);
      
      // Inicializar configuración si es necesario
      await fetch('http://localhost:8000/votos/inicializar-configuracion', {
        method: 'POST'
      });
      
      // Obtener estado actual
      const response = await fetch('http://localhost:8000/votos/estado-mesa');
      
      if (response.ok) {
        const estado = await response.json();
        setEstadoMesa(estado);
      } else {
        console.error('Error obteniendo estado de mesa');
        // Estado por defecto
        setEstadoMesa({
          estado: 'abierta',
          mensaje: 'La mesa de votación está abierta',
          permite_votos: true
        });
      }
    } catch (error) {
      console.error('Error de conexión:', error);
      // Estado por defecto
      setEstadoMesa({
        estado: 'abierta',
        mensaje: 'La mesa de votación está abierta (modo offline)',
        permite_votos: true
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCerrarMesa = async () => {
    if (!motivo.trim()) {
      alert('Por favor ingrese un motivo para cerrar la mesa');
      return;
    }

    const confirmar = confirm(
      '¿Está seguro de que desea cerrar la mesa de votación?\n\n' +
      'Esto impedirá que se registren nuevos votos hasta que la mesa sea reabierta.'
    );
    
    if (!confirmar) return;

    try {
      setProcesando(true);
      
      const response = await fetch('http://localhost:8000/votos/cerrar-mesa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          motivo: motivo.trim()
        })
      });

      if (response.ok) {
        const resultado = await response.json();
        alert('Mesa de votación cerrada exitosamente');
        setMotivo('');
        await cargarEstadoMesa();
      } else {
        const error = await response.text();
        alert(`Error al cerrar la mesa: ${error}`);
      }
    } catch (error) {
      console.error('Error cerrando mesa:', error);
      alert('Error de conexión al cerrar la mesa');
    } finally {
      setProcesando(false);
    }
  };

  const handleAbrirMesa = async () => {
    if (!motivo.trim()) {
      alert('Por favor ingrese un motivo para reabrir la mesa');
      return;
    }

    const confirmar = confirm(
      '¿Está seguro de que desea reabrir la mesa de votación?\n\n' +
      'Esto permitirá que se registren nuevos votos nuevamente.'
    );
    
    if (!confirmar) return;

    try {
      setProcesando(true);
      
      const response = await fetch('http://localhost:8000/votos/abrir-mesa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          motivo: motivo.trim()
        })
      });

      if (response.ok) {
        const resultado = await response.json();
        alert('Mesa de votación reabierta exitosamente');
        setMotivo('');
        await cargarEstadoMesa();
      } else {
        const error = await response.text();
        alert(`Error al reabrir la mesa: ${error}`);
      }
    } catch (error) {
      console.error('Error reabriendo mesa:', error);
      alert('Error de conexión al reabrir la mesa');
    } finally {
      setProcesando(false);
    }
  };

  const handleVolver = () => {
    navigate('/admin');
  };

  if (loading) {
    return (
      <div className="cerrar-mesa-container">
        <div className="cerrar-mesa-content">
          <div className="cerrar-mesa-icon">⏳</div>
          <h2 className="cerrar-mesa-title">Cargando estado de la mesa...</h2>
        </div>
      </div>
    );
  }

  const mesaCerrada = estadoMesa?.estado === 'cerrada';

  return (
    <div className="cerrar-mesa-container">
      <div className="cerrar-mesa-content">
        <div className="cerrar-mesa-icon">
          {mesaCerrada ? '🔒' : '🗳️'}
        </div>
        <h2 className="cerrar-mesa-title">
          {mesaCerrada ? 'Gestionar Mesa Cerrada' : 'Gestionar Mesa de Votación'}
        </h2>
        
        {user && (
          <div className="admin-user-info" style={{
            background: '#f8f9fa', 
            padding: '15px', 
            borderRadius: '8px', 
            marginBottom: '20px', 
            textAlign: 'center', 
            border: '1px solid #e9ecef'
          }}>
            <strong>Presidente:</strong> {user.nombre_completo}
            <br />
            <small>CI: {user.ci} | Gestionando mesa de votación</small>
          </div>
        )}

        {/* Estado actual */}
        <div className={`estado-mesa ${mesaCerrada ? 'cerrada' : 'abierta'}`}>
          <div className="estado-icon">
            {mesaCerrada ? '🔒' : '✅'}
          </div>
          <div className="estado-info">
            <h3>Estado Actual: {mesaCerrada ? 'MESA CERRADA' : 'MESA ABIERTA'}</h3>
            <p>{estadoMesa?.mensaje}</p>
            <p>
              <strong>Votación:</strong> {estadoMesa?.permite_votos ? 'Permitida' : 'Bloqueada'}
            </p>
          </div>
        </div>

        {/* Formulario de acción */}
        <div className="accion-form">
          <label htmlFor="motivo">
            <strong>
              Motivo para {mesaCerrada ? 'reabrir' : 'cerrar'} la mesa:
            </strong>
          </label>
          <textarea
            id="motivo"
            value={motivo}
            onChange={(e) => setMotivo(e.target.value)}
            placeholder={
              mesaCerrada 
                ? "Ejemplo: Extensión del horario de votación por decisión administrativa"
                : "Ejemplo: Finalización del período electoral según cronograma"
            }
            rows={3}
            className="motivo-textarea"
          />
        </div>

        {/* Información de la acción */}
        <div className={`warning-message ${mesaCerrada ? 'info' : 'warning'}`}>
          <strong>{mesaCerrada ? '📋 Reapertura de Mesa' : '⚠️ Cierre de Mesa'}</strong>
          <div className="info-text">
            {mesaCerrada ? (
              <>
                • Se habilitará nuevamente el período de votación<br/>
                • Los votantes podrán registrar sus votos<br/>
                • El sistema volverá a estar operativo<br/>
                • Se registrará el evento de reapertura
              </>
            ) : (
              <>
                • Se finalizará el período de votación<br/>
                • No se permitirán nuevos votos<br/>
                • Los resultados quedarán disponibles<br/>
                • La mesa podrá reabrirse si es necesario
              </>
            )}
          </div>
        </div>

        {/* Botones de acción */}
        <div className="cerrar-mesa-buttons">
          {mesaCerrada ? (
            <button 
              className="cerrar-mesa-button abrir-button" 
              onClick={handleAbrirMesa}
              disabled={procesando || !motivo.trim()}
            >
              {procesando ? '⏳ Reabriendo Mesa...' : '🔓 Reabrir Mesa de Votación'}
            </button>
          ) : (
            <button 
              className="cerrar-mesa-button cerrar-button" 
              onClick={handleCerrarMesa}
              disabled={procesando || !motivo.trim()}
            >
              {procesando ? '⏳ Cerrando Mesa...' : '🔒 Cerrar Mesa de Votación'}
            </button>
          )}
          
          <button 
            className="cerrar-mesa-button cancel-button" 
            onClick={handleVolver}
            disabled={procesando}
          >
            Volver al Panel de Administración
          </button>
        </div>

        {/* Botón para actualizar estado */}
        <div style={{textAlign: 'center', marginTop: '20px'}}>
          <button 
            onClick={cargarEstadoMesa}
            disabled={loading || procesando}
            style={{
              background: '#17a2b8',
              color: 'white',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            🔄 Actualizar Estado
          </button>
        </div>
      </div>
    </div>
  );
}

export default CerrarMesa;
