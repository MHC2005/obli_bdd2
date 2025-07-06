import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import './Autorizar.css';

function Autorizar() {
  const navigate = useNavigate();
  const { user, logout } = useUser();
  const [votosObservados, setVotosObservados] = useState([]);
  const [loading, setLoading] = useState(true);
  const [procesando, setProcesando] = useState(null);

  useEffect(() => {
    // Verificar que el usuario sea presidente
    if (!user || user.rol !== 'presidente') {
      alert('Acceso denegado. Solo el presidente puede autorizar votos.');
      navigate('/login');
      return;
    }

    cargarVotosObservados();
  }, [user, navigate]);

  const cargarVotosObservados = async () => {
    try {
      setLoading(true);
      console.log('Intentando cargar votos observados desde:', 'http://localhost:8000/votos/observados');
      
      const response = await fetch('http://localhost:8000/votos/observados');
      console.log('Respuesta recibida:', response.status, response.statusText);
      
      if (response.ok) {
        const votos = await response.json();
        console.log('Votos observados cargados exitosamente:', votos);
        console.log('Número de votos:', votos.length);
        
        // Verificar si la respuesta es un array válido
        if (Array.isArray(votos)) {
          // Eliminar duplicados por ID de voto (por si acaso)
          const votosUnicos = votos.filter((voto, index, self) => 
            index === self.findIndex(v => v.id_voto === voto.id_voto)
          );
          
          if (votosUnicos.length !== votos.length) {
            console.warn(`Se encontraron ${votos.length - votosUnicos.length} votos duplicados, se eliminaron automáticamente`);
          }
          
          setVotosObservados(votosUnicos);
        } else {
          console.error('La respuesta no es un array válido:', votos);
          setVotosObservados([]);
        }
      } else {
        // Obtener más detalles del error
        const errorText = await response.text();
        console.error('Error cargando votos observados:');
        console.error('Status:', response.status);
        console.error('Status Text:', response.statusText);
        console.error('Error Body:', errorText);
        
        alert(`Error al cargar los votos observados: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      console.error('Error de conexión completo:', error);
      console.error('Tipo de error:', error.name);
      console.error('Mensaje:', error.message);
      
      alert(`Error de conexión al cargar votos observados: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleAprobar = async (idVoto) => {
    if (procesando) return;
    
    const confirmar = confirm('¿Está seguro de que desea aprobar este voto observado?');
    if (!confirmar) return;
    
    try {
      setProcesando(idVoto);
      const response = await fetch(`http://localhost:8000/votos/autorizar/${idVoto}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          decision: 'aprobar',
          motivo: 'Aprobado por el presidente de mesa'
        })
      });

      if (response.ok) {
        const resultado = await response.json();
        console.log('Voto aprobado:', resultado);
        alert(`Voto ${idVoto} aprobado exitosamente. El voto ahora es válido.`);
        
        // Recargar la lista de votos observados
        await cargarVotosObservados();
      } else {
        const error = await response.text();
        console.error('Error aprobando voto:', error);
        alert('Error al aprobar el voto');
      }
    } catch (error) {
      console.error('Error de conexión:', error);
      alert('Error de conexión al aprobar el voto');
    } finally {
      setProcesando(null);
    }
  };

  const handleRechazar = async (idVoto) => {
    if (procesando) return;
    
    const motivo = prompt('Ingrese el motivo del rechazo (opcional):');
    if (motivo === null) return; // Usuario canceló
    
    const confirmar = confirm('¿Está seguro de que desea rechazar este voto observado?');
    if (!confirmar) return;
    
    try {
      setProcesando(idVoto);
      const response = await fetch(`http://localhost:8000/votos/autorizar/${idVoto}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          decision: 'rechazar',
          motivo: motivo || 'Rechazado por el presidente de mesa'
        })
      });

      if (response.ok) {
        const resultado = await response.json();
        console.log('Voto rechazado:', resultado);
        alert(`Voto ${idVoto} rechazado. El voto no será contabilizado.`);
        
        // Recargar la lista de votos observados
        await cargarVotosObservados();
      } else {
        const error = await response.text();
        console.error('Error rechazando voto:', error);
        alert('Error al rechazar el voto');
      }
    } catch (error) {
      console.error('Error de conexión:', error);
      alert('Error de conexión al rechazar el voto');
    } finally {
      setProcesando(null);
    }
  };

  const handleVolver = () => {
    navigate('/admin');
  };

  if (loading) {
    return (
      <div className="autorizar-container">
        <div className="autorizar-content">
          <div className="autorizar-icon">⏳</div>
          <h2 className="autorizar-title">Cargando votos observados...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="autorizar-container">
      <div className="autorizar-content">
        <div className="autorizar-icon">
          👔
        </div>
        <h2 className="autorizar-title">Autorizar Votos Observados</h2>
        
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
            <small>CI: {user.ci} | Autorizando votos observados</small>
          </div>
        )}
        
        {votosObservados.length > 0 ? (
          <div className="status-message pending">
            <strong>Votos Observados:</strong> {votosObservados.length} 
            {votosObservados.length === 1 ? ' voto requiere' : ' votos requieren'} 
            tu autorización como Presidente de Mesa.
          </div>
        ) : (
          <div className="status-message">
            <strong>¡Todo al día!</strong> No hay votos observados pendientes de autorización en este momento.
          </div>
        )}

        <div className="solicitudes-container">
          {votosObservados.length > 0 ? (
            votosObservados.map((voto) => (
              <div key={voto.id_voto} className="solicitud-item">
                <div className="solicitud-header">
                  <div className="solicitud-ci">
                    👤 {voto.nombre_completo} (CI: {voto.ci})
                  </div>
                  <div className="solicitud-estado">
                    {voto.estado}
                  </div>
                </div>
                
                <div className="solicitud-detalles">
                  <strong>Lista votada:</strong> {voto.numero_lista}<br/>
                  <strong>Elección:</strong> {voto.tipo_eleccion}<br/>
                  <strong>Ubicación:</strong> {voto.barrio}, {voto.departamento}<br/>
                  <strong>Fecha:</strong> {new Date(voto.fecha_hora_emision).toLocaleString('es-UY')}<br/>
                  <strong>ID Voto:</strong> {voto.id_voto}
                </div>
                
                <div className="solicitud-acciones">
                  <button 
                    className="autorizar-button aprobar"
                    onClick={() => handleAprobar(voto.id_voto)}
                    disabled={procesando === voto.id_voto}
                  >
                    {procesando === voto.id_voto ? '⏳ Procesando...' : '✅ Aprobar Voto'}
                  </button>
                  <button 
                    className="autorizar-button rechazar"
                    onClick={() => handleRechazar(voto.id_voto)}
                    disabled={procesando === voto.id_voto}
                  >
                    {procesando === voto.id_voto ? '⏳ Procesando...' : '❌ Rechazar Voto'}
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="empty-state">
              <div className="empty-state-icon">📝</div>
              <div className="empty-state-text">
                No hay votos observados pendientes de autorización.
              </div>
            </div>
          )}
        </div>

        {/* Botón para recargar */}
        <div style={{textAlign: 'center', margin: '20px 0'}}>
          <button 
            className="autorizar-button refresh"
            onClick={cargarVotosObservados}
            disabled={loading}
            style={{
              background: '#ffc107',
              color: '#212529',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              marginRight: '10px'
            }}
          >
            🔄 Actualizar Lista
          </button>
          
          {/* Botón temporal para crear voto de prueba */}
          <button 
            onClick={async () => {
              try {
                const response = await fetch('http://localhost:8000/votos/crear-voto-observado-prueba', {
                  method: 'POST'
                });
                if (response.ok) {
                  alert('Voto observado de prueba creado');
                  await cargarVotosObservados();
                } else {
                  alert('Error creando voto de prueba');
                }
              } catch (error) {
                alert('Error de conexión');
              }
            }}
            style={{
              background: '#28a745',
              color: 'white',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            🧪 Crear Voto de Prueba
          </button>
        </div>

        <div className="autorizar-nav">
          <button className="nav-button" onClick={handleVolver}>
            Volver al Panel de Administración
          </button>
        </div>
      </div>
    </div>
  );
}

export default Autorizar;
