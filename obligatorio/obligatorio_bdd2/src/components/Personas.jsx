import React, { useEffect, useState } from "react";

const Personas = () => {
  const [personas, setPersonas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
fetch("http://127.0.0.1:8000/personas")
      .then((res) => {
        if (!res.ok) throw new Error("Error al obtener personas");
        return res.json();
      })
      .then((data) => {
        setPersonas(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Cargando personas...</p>;

  return (
    <div>
      <h2>Lista de Personas</h2>
      <table>
        <thead>
          <tr>
            <th>CI</th>
            <th>Nombre Completo</th>
            <th>Número</th>
            <th>Serie</th>
          </tr>
        </thead>
        <tbody>
          {personas.map((p) => (
            <tr key={p.CI}>
              <td>{p.CI}</td>
              <td>{p.Nombre_Completo}</td>
              <td>{p.Numero}</td>
              <td>{p.Serie}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Personas;
