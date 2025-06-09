function Votar() {
  const handleVote = (e) => {
    e.preventDefault();
    // En el futuro: enviar voto al backend con fetch
    alert('Voto emitido con éxito');
  };

  return (
    <div>
      <h2>Emitir Voto</h2>
      <form onSubmit={handleVote}>
        <select required>
          <option value="">-- Seleccione una lista --</option>
          <option value="1">Lista 1 - Partido A</option>
          <option value="2">Lista 2 - Partido B</option>
        </select>
        <button type="submit">Votar</button>
      </form>
    </div>
  );
}

export default Votar;
