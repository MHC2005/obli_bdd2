from fastapi import APIRouter, Depends
from sqlalchemy import text
from ..database import engine

"""
ENDPOINTS DISPONIBLES EN PARTIDOS:
✅ GET /partidos/ - Listar todos los partidos políticos con presidentes/vicepresidentes
✅ GET /partidos/{id_partido} - Obtener partido específico por ID
✅ GET /partidos/{id_partido}/listas - Listas electorales de un partido político
"""

router = APIRouter(prefix="/partidos", tags=["Partidos Políticos"])

def get_db():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@router.get("/")
def listar_partidos(db = Depends(get_db)):
    query = text("""
        SELECT pp.id_partido_politico, pp.nombre, pp.direccion_sede,
               p1.nombre_completo as presidente_nombre,
               p2.nombre_completo as vicepresidente_nombre
        FROM partido_politico pp
        LEFT JOIN persona p1 ON pp.ci_presidente = p1.ci
        LEFT JOIN persona p2 ON pp.ci_vicepresidente = p2.ci
        ORDER BY pp.nombre
    """)
    result = db.execute(query)
    partidos = []
    for row in result:
        partidos.append({
            "id_partido_politico": row.id_partido_politico,
            "nombre": row.nombre,
            "direccion_sede": row.direccion_sede,
            "presidente_nombre": row.presidente_nombre,
            "vicepresidente_nombre": row.vicepresidente_nombre
        })
    return partidos

@router.get("/{id_partido}")
def obtener_partido_por_id(id_partido: int, db = Depends(get_db)):
    query = text("""
        SELECT pp.id_partido_politico, pp.nombre, pp.direccion_sede,
               pp.ci_presidente, pp.ci_vicepresidente,
               p1.nombre_completo as presidente_nombre,
               p2.nombre_completo as vicepresidente_nombre
        FROM partido_politico pp
        LEFT JOIN persona p1 ON pp.ci_presidente = p1.ci
        LEFT JOIN persona p2 ON pp.ci_vicepresidente = p2.ci
        WHERE pp.id_partido_politico = :id
    """)
    result = db.execute(query, {"id": id_partido})
    row = result.fetchone()
    
    if row is None:
        return {"error": f"No se encontró partido con ID: {id_partido}"}
    
    return {
        "id_partido_politico": row.id_partido_politico,
        "nombre": row.nombre,
        "direccion_sede": row.direccion_sede,
        "ci_presidente": row.ci_presidente,
        "ci_vicepresidente": row.ci_vicepresidente,
        "presidente_nombre": row.presidente_nombre,
        "vicepresidente_nombre": row.vicepresidente_nombre
    }

@router.get("/{id_partido}/listas")
def obtener_listas_por_partido(id_partido: int, db = Depends(get_db)):
    query = text("""
        SELECT l.numero_lista, l.organ, l.departamento,
               p.nombre_completo as candidato_nombre
        FROM lista l
        LEFT JOIN candidato c ON l.ci = c.ci
        LEFT JOIN persona p ON c.ci = p.ci
        WHERE l.id_partido_politico = :id_partido
        ORDER BY l.numero_lista
    """)
    result = db.execute(query, {"id_partido": id_partido})
    listas = []
    for row in result:
        listas.append({
            "numero_lista": row.numero_lista,
            "organ": row.organ,
            "departamento": row.departamento,
            "candidato_nombre": row.candidato_nombre
        })
    return listas
