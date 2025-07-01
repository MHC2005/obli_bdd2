import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import './Votar.css';

function Votar() {
  const navigate = useNavigate();
  const { user } = useUser();
  const [selectedOption, setSelectedOption] = useState('');
  const [isVoting, setIsVoting] = useState(false);
  const [listas, setListas] = useState([]);
  const [eleccionActiva, setEleccionActiva] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Cargar listas electorales y elección activa
    const cargarDatos = async () => {
      try {
        console.log('Iniciando carga de datos...');
        console.log('Usuario actual:', user);
        
        // Obtener listas electorales (sin autenticación requerida)
        const resListas = await fetch('http://localhost:8000/votos/listas');
        
        console.log('Respuesta listas:', resListas.status);
        if (resListas.ok) {
          const listasData = await resListas.json();
          console.log('Listas obtenidas:', listasData);
          setListas(listasData);
        } else {
          const errorListas = await resListas.text();
          console.error('Error obteniendo listas:', errorListas);
          alert('Error al cargar las listas electorales');
        }

        // Obtener elección activa (sin autenticación requerida)
        const resEleccion = await fetch('http://localhost:8000/elecciones/activa');
        
        console.log('Respuesta elección activa:', resEleccion.status);
        if (resEleccion.ok) {
          const eleccion = await resEleccion.json();
          console.log('Elección activa obtenida:', eleccion);
          // Verificar si hay error en la respuesta
          if (eleccion.error) {
            console.error('Error en elección activa:', eleccion.error);
            // No mostrar alert, solo log. Continuamos sin elección activa.
            console.warn('Continuando sin elección activa definida');
          } else {
            setEleccionActiva(eleccion);
          }
        } else {
          const errorEleccion = await resEleccion.text();
          console.error('Error obteniendo elección activa:', errorEleccion);
          // En lugar de mostrar error, vamos a intentar usar la primera elección disponible
          try {
            const resElecciones = await fetch('http://localhost:8000/elecciones/');
            if (resElecciones.ok) {
              const elecciones = await resElecciones.json();
              if (elecciones.length > 0) {
                console.log('Usando primera elección disponible:', elecciones[0]);
                setEleccionActiva(elecciones[0]);
              } else {
                console.error('No hay elecciones disponibles en el sistema');
              }
            }
          } catch (fallbackError) {
            console.error('Error obteniendo elecciones de fallback:', fallbackError);
          }
        }
      } catch (error) {
        console.error('Error cargando datos:', error);
        alert('Error de conexión al cargar las opciones de votación: ' + error.message);
      } finally {
        setLoading(false);
      }
    };

    cargarDatos();
  }, [user]);

  const handleVote = async (e) => {
    e.preventDefault();
    
    // Validaciones iniciales
    if (!selectedOption) {
      alert('Por favor seleccione una opción antes de votar.');
      return;
    }

    if (!user) {
      alert('Error: Usuario no autenticado. Por favor inicie sesión nuevamente.');
      navigate('/login');
      return;
    }

    if (!eleccionActiva) {
      alert('Error: No hay elección activa disponible.');
      return;
    }

    console.log('=== INICIO DEL PROCESO DE VOTACIÓN ===');
    console.log('Usuario:', user);
    console.log('Elección activa:', eleccionActiva);
    console.log('Lista seleccionada:', selectedOption);

    if (!user.id_circuito || !eleccionActiva.id_eleccion) {
      console.error('Información faltante:', { 
        user_id_circuito: user.id_circuito, 
        eleccion_id: eleccionActiva.id_eleccion 
      });
      alert('Error: Información de votación incompleta. Verifique su sesión.');
      return;
    }

    setIsVoting(true);
    
    try {
      const votoData = {
        numero_lista: parseInt(selectedOption),
        id_eleccion: eleccionActiva.id_eleccion,
        id_circuito: user.id_circuito,
        estado: "Válido",
        observado: false
      };

      console.log('Datos del voto a enviar:', votoData);

      const response = await fetch('http://localhost:8000/votos/registrar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(votoData)
      });

      console.log('Respuesta del servidor - Status:', response.status);
      console.log('Respuesta del servidor - Headers:', Object.fromEntries(response.headers.entries()));

      if (response.ok) {
        const result = await response.json();
        console.log('Voto registrado exitosamente:', result);
        alert('¡Voto emitido con éxito! Gracias por participar en el proceso democrático.');
        navigate('/home');
      } else {
        const errorText = await response.text();
        console.error('Error del servidor (texto completo):', errorText);
        
        try {
          const error = JSON.parse(errorText);
          console.error('Error del servidor (parseado):', error);
          alert(`Error al registrar voto: ${error.detail || 'Error desconocido'}`);
        } catch (parseError) {
          console.error('Error parseando respuesta de error:', parseError);
          alert(`Error al registrar voto: ${errorText}`);
        }
      }
    } catch (error) {
      console.error('Error de conexión:', error);
      alert(`Error de conexión al registrar el voto: ${error.message}\n\nVerifique que el servidor esté funcionando en http://localhost:8000`);
    } finally {
      setIsVoting(false);
      console.log('=== FIN DEL PROCESO DE VOTACIÓN ===');
    }
  };

  const handleSelectChange = (e) => {
    setSelectedOption(e.target.value);
  };

  const handleVolver = () => {
    navigate('/home');
  };

  if (loading) {
    return (
      <div className="votar-container">
        <div className="votar-content">
          <div className="votar-icon">⏳</div>
          <h2 className="votar-title">Cargando opciones de votación...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="votar-container">
      <div className="votar-content">
        <div className="votar-icon">
          🗳️
        </div>
        <h2 className="votar-title">Emitir Voto</h2>
        
        {eleccionActiva && (
          <div className="eleccion-info">
            <strong>Elección:</strong> {eleccionActiva.tipo} - {eleccionActiva.fecha}
          </div>
        )}
        
        {user && (
          <div className="usuario-info">
            <strong>Votando en:</strong> {user.barrio}, {user.departamento}
            <br />
            <small>Circuito: {user.id_circuito} | CI: {user.ci}</small>
          </div>
        )}
        
        <div className="votar-instructions">
          <strong>Instrucciones:</strong> Seleccione cuidadosamente la lista de su preferencia. 
          Una vez confirmado su voto, no podrá modificarlo.
        </div>

        {user && eleccionActiva && (
          <div className="warning-info" style={{background: '#fff3cd', padding: '10px', margin: '10px 0', borderRadius: '5px', border: '1px solid #ffeaa7'}}>
            ⚠️ <strong>Importante:</strong> Solo puede votar una vez por elección. Asegúrese de su selección antes de confirmar.
          </div>
        )}
        
        {!eleccionActiva && !loading && (
          <div className="error-info" style={{background: '#f8d7da', padding: '10px', margin: '10px 0', borderRadius: '5px', border: '1px solid #f5c6cb'}}>
            ❌ <strong>Error:</strong> No hay elecciones activas disponibles en este momento.
            <br />
            <button 
              onClick={async () => {
                try {
                  const res = await fetch('http://localhost:8000/elecciones/');
                  if (res.ok) {
                    const elecciones = await res.json();
                    if (elecciones.length > 0) {
                      // Usar la primera elección como fallback
                      setEleccionActiva(elecciones[0]);
                      console.log('Elección seleccionada manualmente:', elecciones[0]);
                    }
                  }
                } catch (error) {
                  console.error('Error cargando elecciones:', error);
                }
              }}
              style={{fontSize: '12px', padding: '5px 10px', marginTop: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '3px', cursor: 'pointer'}}
            >
              🔄 Cargar Elección Disponible
            </button>
          </div>
        )}
        
        {listas.length === 0 && !loading && (
          <div className="error-info" style={{background: '#f8d7da', padding: '10px', margin: '10px 0', borderRadius: '5px', border: '1px solid #f5c6cb'}}>
            ❌ <strong>Error:</strong> No hay listas electorales disponibles.
          </div>
        )}
        
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
              {listas.map((lista) => (
                <option key={lista.numero_lista} value={lista.numero_lista}>
                  Lista {lista.numero_lista} - {lista.partido_nombre || 'Partido Independiente'}
                  {lista.candidato_nombre && ` (${lista.candidato_nombre})`}
                </option>
              ))}
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
