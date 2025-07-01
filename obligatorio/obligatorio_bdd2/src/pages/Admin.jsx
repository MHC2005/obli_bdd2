import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import './Admin.css';

function Admin() {
  const navigate = useNavigate();
  const { user, logout } = useUser();
  const [estadisticas, setEstadisticas] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar que el usuario sea presidente
    if (!user || user.rol !== 'presidente') {
      alert('Acceso denegado. Solo el presidente puede acceder a esta sección.');
      navigate('/login');
      return;
    }

    // Cargar estadísticas del sistema
    cargarEstadisticas();
  }, [user, navigate]);

  const cargarEstadisticas = async () => {
    try {
      // Obtener todas las elecciones
      const resElecciones = await fetch('http://localhost:8000/elecciones/');
      const elecciones = resElecciones.ok ? await resElecciones.json() : [];

      // Obtener todos los votos
      const resVotos = await fetch('http://localhost:8000/votos/');
      const votos = resVotos.ok ? await resVotos.json() : [];

      // Obtener todas las listas
      const resListas = await fetch('http://localhost:8000/votos/listas');
      const listas = resListas.ok ? await resListas.json() : [];

      setEstadisticas({
        totalElecciones: elecciones.length,
        totalVotos: votos.length,
        totalListas: listas.length,
        elecciones: elecciones,
        votos: votos,
        listas: listas
      });
    } catch (error) {
      console.error('Error cargando estadísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleCerrarMesa = () => {
    navigate('/cerrar-mesa');
  };

  const handleAutorizar = () => {
    navigate('/autorizar');
  };

  const handleVerResultados = () => {
    // Implementar navegación a resultados
    alert('Función de resultados en desarrollo');
  };

  if (loading) {
    return (
      <div className="admin-container">
        <div className="admin-content">
          <div className="admin-icon">⏳</div>
          <h2 className="admin-title">Cargando panel de administración...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <div className="admin-content">
        <div className="admin-header">
          <div className="admin-icon">👨‍💼</div>
          <h1 className="admin-title">Panel de Administración</h1>
          <h2 className="admin-subtitle">Sistema Electoral - Acceso Presidencial</h2>
        </div>

        {user && (
          <div className="admin-user-info">
            <strong>🔐 Acceso Autorizado:</strong> {user.nombre_completo}
            <br />
            <small>CI: {user.ci} | Rol: {user.rol.toUpperCase()}</small>
            <br />
            <small>⚡ Permisos completos del sistema</small>
          </div>
        )}

        {/* Estadísticas del sistema */}
        {estadisticas && (
          <div className="admin-stats">
            <h3>📊 Estadísticas del Sistema</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-number">{estadisticas.totalElecciones}</div>
                <div className="stat-label">Elecciones</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{estadisticas.totalVotos}</div>
                <div className="stat-label">Votos Emitidos</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{estadisticas.totalListas}</div>
                <div className="stat-label">Listas Electorales</div>
              </div>
            </div>
          </div>
        )}

        {/* Opciones de administración */}
        <div className="admin-actions">
          <h3>⚙️ Funciones de Administración</h3>
          
          <div className="action-buttons">
            <button 
              className="admin-button primary"
              onClick={handleCerrarMesa}
            >
              🔒 Cerrar Mesa de Votación
            </button>

            <button 
              className="admin-button secondary"
              onClick={handleAutorizar}
            >
              ✅ Autorizar Votantes
            </button>

            <button 
              className="admin-button info"
              onClick={handleVerResultados}
            >
              📈 Ver Resultados
            </button>

            <button 
              className="admin-button refresh"
              onClick={cargarEstadisticas}
            >
              🔄 Actualizar Estadísticas
            </button>
          </div>
        </div>

        {/* Información de elecciones */}
        {estadisticas && estadisticas.elecciones.length > 0 && (
          <div className="admin-elections">
            <h3>🗳️ Elecciones en el Sistema</h3>
            <div className="elections-list">
              {estadisticas.elecciones.map((eleccion) => (
                <div key={eleccion.id_eleccion} className="election-card">
                  <strong>{eleccion.tipo}</strong>
                  <br />
                  <small>Fecha: {eleccion.fecha}</small>
                  <br />
                  <small>ID: {eleccion.id_eleccion}</small>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Botón de cerrar sesión */}
        <div className="admin-logout">
          <button 
            className="admin-button danger"
            onClick={handleLogout}
          >
            🚪 Cerrar Sesión
          </button>
        </div>
      </div>
    </div>
  );
}

export default Admin;
