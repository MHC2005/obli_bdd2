function CerrarMesa() {
  const handleCerrar = () => {
    // En el futuro: petición al backend
    alert('Mesa cerrada. No se permiten más votos.');
  };

  return (
    <div>
      <h2>Cerrar Mesa de Votación</h2>
      <button onClick={handleCerrar}>Cerrar Mesa</button>
    </div>
  );
}

export default CerrarMesa;
