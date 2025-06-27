from fastapi import APIRouter, Depends
from sqlalchemy import text
from ..database import engine

"""
ENDPOINTS DISPONIBLES EN ELECCIONES:
✅ GET /elecciones/ - Listar todas las elecciones ordenadas por fecha
✅ GET /elecciones/{id_eleccion} - Obtener elección específica por ID
✅ GET /elecciones/{id_eleccion}/candidatos - Candidatos que se presentan en una elección
"""

router = APIRouter(prefix="/elecciones", tags=["Elecciones"])

def get_db():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@router.get("/")
def listar_elecciones(db = Depends(get_db)):
    query = text("SELECT id_eleccion, fecha, tipo FROM eleccion ORDER BY fecha DESC")
    result = db.execute(query)
    elecciones = []
    for row in result:
        elecciones.append({
            "id_eleccion": row.id_eleccion,
            "fecha": row.fecha,
            "tipo": row.tipo
        })
    return elecciones

@router.get("/{id_eleccion}")
def obtener_eleccion_por_id(id_eleccion: int, db = Depends(get_db)):
    query = text("SELECT id_eleccion, fecha, tipo FROM eleccion WHERE id_eleccion = :id")
    result = db.execute(query, {"id": id_eleccion})
    row = result.fetchone()
    
    if row is None:
        return {"error": f"No se encontró elección con ID: {id_eleccion}"}
    
    return {
        "id_eleccion": row.id_eleccion,
        "fecha": row.fecha,
        "tipo": row.tipo
    }

@router.get("/{id_eleccion}/candidatos")
def obtener_candidatos_por_eleccion(id_eleccion: int, db = Depends(get_db)):
    query = text("""
        SELECT p.ci, p.nombre_completo, c.cargo_postulado
        FROM persona p
        INNER JOIN candidato c ON p.ci = c.ci
        INNER JOIN presentan pr ON c.ci = pr.ci
        WHERE pr.id_eleccion = :id_eleccion
        ORDER BY p.nombre_completo
    """)
    result = db.execute(query, {"id_eleccion": id_eleccion})
    candidatos = []
    for row in result:
        candidatos.append({
            "ci": row.ci,
            "nombre_completo": row.nombre_completo,
            "cargo_postulado": row.cargo_postulado
        })
    return candidatos
