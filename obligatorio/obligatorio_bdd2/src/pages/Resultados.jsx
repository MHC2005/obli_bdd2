import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import './Resultados.css';

function Resultados() {
  const navigate = useNavigate();
  const { user } = useUser();
  const [resultados, setResultados] = useState([]);
  const [elecciones, setElecciones] = useState([]);
  const [eleccionSeleccionada, setEleccionSeleccionada] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadingResultados, setLoadingResultados] = useState(false);
  const [totalVotos, setTotalVotos] = useState(0);

  useEffect(() => {
    // Verificar que el usuario sea presidente
    if (!user || user.rol !== 'presidente') {
      alert('Acceso denegado. Solo el presidente puede ver los resultados.');
      navigate('/login');
      return;
    }

    cargarElecciones();
  }, [user, navigate]);

  const cargarElecciones = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/elecciones/');
      
      if (response.ok) {
        const eleccionesData = await response.json();
        setElecciones(eleccionesData);
        
        // Si hay elecciones, seleccionar la primera por defecto
        if (eleccionesData.length > 0) {
          setEleccionSeleccionada(eleccionesData[0].id_eleccion);
          await cargarResultados(eleccionesData[0].id_eleccion);
        }
      } else {
        alert('Error al cargar las elecciones');
      }
    } catch (error) {
      console.error('Error cargando elecciones:', error);
      alert('Error de conexión al cargar elecciones');
    } finally {
      setLoading(false);
    }
  };

  const cargarResultados = async (idEleccion) => {
    try {
      setLoadingResultados(true);
      
      // Obtener todos los votos de la elección
      const response = await fetch(`http://localhost:8000/votos/eleccion/${idEleccion}`);
      
      if (response.ok) {
        const votos = await response.json();
        
        // Procesar resultados por lista
        const resultadosPorLista = {};
        let totalVotosValidos = 0;
        
        votos.forEach(voto => {
          if (voto.estado === 'Válido') {
            const numeroLista = voto.numero_lista;
            if (!resultadosPorLista[numeroLista]) {
              resultadosPorLista[numeroLista] = {
                numero_lista: numeroLista,
                nombre_lista: voto.nombre_lista || `Lista ${numeroLista}`,
                votos: 0,
                porcentaje: 0
              };
            }
            resultadosPorLista[numeroLista].votos++;
            totalVotosValidos++;
          }
        });
        
        // Calcular porcentajes
        const resultadosArray = Object.values(resultadosPorLista).map(lista => ({
          ...lista,
          porcentaje: totalVotosValidos > 0 ? ((lista.votos / totalVotosValidos) * 100).toFixed(2) : 0
        }));
        
        // Ordenar por número de votos (descendente)
        resultadosArray.sort((a, b) => b.votos - a.votos);
        
        setResultados(resultadosArray);
        setTotalVotos(totalVotosValidos);
      } else {
        alert('Error al cargar los resultados');
      }
    } catch (error) {
      console.error('Error cargando resultados:', error);
      alert('Error de conexión al cargar resultados');
    } finally {
      setLoadingResultados(false);
    }
  };

  const handleCambiarEleccion = async (e) => {
    const idEleccion = parseInt(e.target.value);
    setEleccionSeleccionada(idEleccion);
    await cargarResultados(idEleccion);
  };

  const handleVolver = () => {
    navigate('/admin');
  };

  if (loading) {
    return (
      <div className="resultados-container">
        <div className="resultados-content">
          <div className="resultados-icon">⏳</div>
          <h2 className="resultados-title">Cargando resultados...</h2>
        </div>
      </div>
    );
  }

  const eleccionActual = elecciones.find(e => e.id_eleccion === eleccionSeleccionada);

  return (
    <div className="resultados-container">
      <div className="resultados-content">
        <div className="resultados-icon">📊</div>
        <h2 className="resultados-title">Resultados Electorales</h2>
        
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
            <small>CI: {user.ci} | Consultando resultados electorales</small>
          </div>
        )}

        {/* Selector de elección */}
        {elecciones.length > 0 && (
          <div className="eleccion-selector">
            <label htmlFor="eleccion-select">
              <strong>Seleccionar Elección:</strong>
            </label>
            <select 
              id="eleccion-select"
              value={eleccionSeleccionada || ''}
              onChange={handleCambiarEleccion}
              className="eleccion-select"
            >
              {elecciones.map(eleccion => (
                <option key={eleccion.id_eleccion} value={eleccion.id_eleccion}>
                  {eleccion.tipo} - {eleccion.fecha} (ID: {eleccion.id_eleccion})
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Información de la elección actual */}
        {eleccionActual && (
          <div className="eleccion-info">
            <h3>🗳️ {eleccionActual.tipo}</h3>
            <p><strong>Fecha:</strong> {eleccionActual.fecha}</p>
            <p><strong>Total de Votos Válidos:</strong> {totalVotos}</p>
          </div>
        )}

        {/* Resultados */}
        {loadingResultados ? (
          <div className="loading-resultados">
            <div className="loading-icon">⏳</div>
            <p>Cargando resultados...</p>
          </div>
        ) : (
          <div className="resultados-section">
            {resultados.length > 0 ? (
              <>
                <h3>📈 Resultados por Lista</h3>
                <div className="resultados-lista">
                  {resultados.map((lista, index) => (
                    <div key={lista.numero_lista} className={`resultado-item ${index === 0 ? 'ganador' : ''}`}>
                      <div className="resultado-header">
                        <div className="lista-info">
                          <span className="numero-lista">Lista {lista.numero_lista}</span>
                          <span className="nombre-lista">{lista.nombre_lista}</span>
                        </div>
                        <div className="posicion">
                          {index === 0 && '🥇'}
                          {index === 1 && '🥈'}
                          {index === 2 && '🥉'}
                          {index > 2 && `#${index + 1}`}
                        </div>
                      </div>
                      
                      <div className="resultado-datos">
                        <div className="votos-count">
                          <strong>{lista.votos}</strong> votos
                        </div>
                        <div className="porcentaje">
                          {lista.porcentaje}%
                        </div>
                      </div>
                      
                      <div className="barra-progreso">
                        <div 
                          className="barra-fill"
                          style={{
                            width: `${lista.porcentaje}%`,
                            backgroundColor: index === 0 ? '#28a745' : index === 1 ? '#ffc107' : index === 2 ? '#fd7e14' : '#6c757d'
                          }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Resumen */}
                <div className="resumen-resultados">
                  <h4>📋 Resumen</h4>
                  <div className="resumen-stats">
                    <div className="stat-item">
                      <strong>Listas Participantes:</strong> {resultados.length}
                    </div>
                    <div className="stat-item">
                      <strong>Total Votos Válidos:</strong> {totalVotos}
                    </div>
                    {resultados.length > 0 && (
                      <div className="stat-item ganador-info">
                        <strong>🏆 Lista Ganadora:</strong> Lista {resultados[0].numero_lista} con {resultados[0].votos} votos ({resultados[0].porcentaje}%)
                      </div>
                    )}
                  </div>
                </div>
              </>
            ) : (
              <div className="no-resultados">
                <div className="no-resultados-icon">🗳️</div>
                <h3>Sin Resultados</h3>
                <p>No hay votos válidos registrados para esta elección.</p>
              </div>
            )}
          </div>
        )}

        {/* Botón para actualizar */}
        <div style={{textAlign: 'center', margin: '20px 0'}}>
          <button 
            onClick={() => cargarResultados(eleccionSeleccionada)}
            disabled={loadingResultados || !eleccionSeleccionada}
            style={{
              background: '#17a2b8',
              color: 'white',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              marginRight: '10px'
            }}
          >
            🔄 Actualizar Resultados
          </button>
        </div>

        <div className="resultados-nav">
          <button className="nav-button" onClick={handleVolver}>
            Volver al Panel de Administración
          </button>
        </div>
      </div>
    </div>
  );
}

export default Resultados;
