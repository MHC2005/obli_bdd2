from fastapi import APIRouter, Depends
from sqlalchemy import text
from ..database import engine

"""
ENDPOINTS DISPONIBLES EN CIRCUITOS:
✅ GET /circuitos/ - Listar todos los circuitos con info de establecimientos
✅ GET /circuitos/{id_circuito} - Obtener circuito específico por ID
✅ GET /circuitos/{id_circuito}/ciudadanos - Ciudadanos habilitados en un circuito
✅ GET /circuitos/{id_circuito}/miembros-mesa - Autoridades de mesa de un circuito
"""

router = APIRouter(prefix="/circuitos", tags=["Circuitos"])

def get_db():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@router.get("/")
def listar_circuitos(db = Depends(get_db)):
    query = text("""
        SELECT c.id_circuito, c.barrio, c.accesible, c.localidad, c.departamento,
               e.nombre as establecimiento_nombre, e.direccion
        FROM circuito c
        LEFT JOIN establecimiento e ON c.id_establecimiento = e.id_establecimiento
        ORDER BY c.departamento, c.localidad, c.barrio
    """)
    result = db.execute(query)
    circuitos = []
    for row in result:
        circuitos.append({
            "id_circuito": row.id_circuito,
            "barrio": row.barrio,
            "accesible": row.accesible,
            "localidad": row.localidad,
            "departamento": row.departamento,
            "establecimiento_nombre": row.establecimiento_nombre,
            "direccion": row.direccion
        })
    return circuitos

@router.get("/{id_circuito}")
def obtener_circuito_por_id(id_circuito: int, db = Depends(get_db)):
    query = text("""
        SELECT c.id_circuito, c.barrio, c.accesible, c.localidad, c.departamento,
               e.nombre as establecimiento_nombre, e.direccion, e.tipo as establecimiento_tipo
        FROM circuito c
        LEFT JOIN establecimiento e ON c.id_establecimiento = e.id_establecimiento
        WHERE c.id_circuito = :id
    """)
    result = db.execute(query, {"id": id_circuito})
    row = result.fetchone()
    
    if row is None:
        return {"error": f"No se encontró circuito con ID: {id_circuito}"}
    
    return {
        "id_circuito": row.id_circuito,
        "barrio": row.barrio,
        "accesible": row.accesible,
        "localidad": row.localidad,
        "departamento": row.departamento,
        "establecimiento_nombre": row.establecimiento_nombre,
        "direccion": row.direccion,
        "establecimiento_tipo": row.establecimiento_tipo
    }

@router.get("/{id_circuito}/ciudadanos")
def obtener_ciudadanos_por_circuito(id_circuito: int, db = Depends(get_db)):
    query = text("""
        SELECT p.ci, p.nombre_completo, c.fecha_nacimiento
        FROM persona p
        INNER JOIN ciudadano c ON p.ci = c.ci
        WHERE c.id_circuito = :id_circuito
        ORDER BY p.nombre_completo
    """)
    result = db.execute(query, {"id_circuito": id_circuito})
    ciudadanos = []
    for row in result:
        ciudadanos.append({
            "ci": row.ci,
            "nombre_completo": row.nombre_completo,
            "fecha_nacimiento": row.fecha_nacimiento
        })
    return ciudadanos

@router.get("/{id_circuito}/miembros-mesa")
def obtener_miembros_mesa_por_circuito(id_circuito: int, db = Depends(get_db)):
    query = text("""
        SELECT p.ci, p.nombre_completo, mm.organismo_estado, i.cargo
        FROM persona p
        INNER JOIN miembro_mesa mm ON p.ci = mm.ci
        INNER JOIN integra i ON mm.ci = i.ci
        WHERE i.id_circuito = :id_circuito
        ORDER BY i.cargo, p.nombre_completo
    """)
    result = db.execute(query, {"id_circuito": id_circuito})
    miembros = []
    for row in result:
        miembros.append({
            "ci": row.ci,
            "nombre_completo": row.nombre_completo,
            "organismo_estado": row.organismo_estado,
            "cargo": row.cargo
        })
    return miembros
