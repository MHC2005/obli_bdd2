from fastapi import APIRouter, Depends
from sqlalchemy import text
from ..database import engine

router = APIRouter(prefix="/personas", tags=["Personas"])

def get_db():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@router.get("/")
def listar_personas(db = Depends(get_db)):
    query = text("SELECT ci, nombre_completo, numero, serie FROM persona")
    result = db.execute(query)
    personas = []
    for row in result:
        personas.append({
            "ci": row.ci,
            "nombre_completo": row.nombre_completo,
            "numero": row.numero,
            "serie": row.serie
        })
    return personas

@router.get("/{ci}")
def obtener_persona_por_ci(ci: int, db = Depends(get_db)):
    query = text("SELECT ci, nombre_completo, numero, serie FROM persona WHERE ci = :ci")
    result = db.execute(query, {"ci": ci})
    row = result.fetchone()
    
    if row is None:
        return {"error": f"No se encontró persona con CI: {ci}"}
    
    return {
        "ci": row.ci,
        "nombre_completo": row.nombre_completo,
        "numero": row.numero,
        "serie": row.serie
    }
