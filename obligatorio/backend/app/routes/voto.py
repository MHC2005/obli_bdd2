from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from ..database import engine
from datetime import datetime

"""
ENDPOINTS DISPONIBLES EN VOTOS:
✅ GET /votos/ - Listar todos los votos ordenados por fecha
✅ GET /votos/eleccion/{id_eleccion} - Votos de una elección específica con info de listas
✅ GET /votos/circuito/{id_circuito} - Votos de un circuito específico
✅ POST /votos/registrar - Registrar un nuevo voto (único POST permitido)
"""

router = APIRouter(prefix="/votos", tags=["Votos"])

def get_db():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@router.get("/")
def listar_votos(db = Depends(get_db)):
    query = text("""
        SELECT v.id_voto, v.fecha_hora_emision, v.observado, v.estado,
               v.id_eleccion, v.id_circuito, v.numero_lista
        FROM voto v
        ORDER BY v.fecha_hora_emision DESC
    """)
    result = db.execute(query)
    votos = []
    for row in result:
        votos.append({
            "id_voto": row.id_voto,
            "fecha_hora_emision": row.fecha_hora_emision,
            "observado": row.observado,
            "estado": row.estado,
            "id_eleccion": row.id_eleccion,
            "id_circuito": row.id_circuito,
            "numero_lista": row.numero_lista
        })
    return votos

@router.get("/eleccion/{id_eleccion}")
def obtener_votos_por_eleccion(id_eleccion: int, db = Depends(get_db)):
    query = text("""
        SELECT v.id_voto, v.fecha_hora_emision, v.observado, v.estado,
               v.id_circuito, v.numero_lista, l.organ, l.departamento
        FROM voto v
        LEFT JOIN lista l ON v.numero_lista = l.numero_lista
        WHERE v.id_eleccion = :id_eleccion
        ORDER BY v.fecha_hora_emision
    """)
    result = db.execute(query, {"id_eleccion": id_eleccion})
    votos = []
    for row in result:
        votos.append({
            "id_voto": row.id_voto,
            "fecha_hora_emision": row.fecha_hora_emision,
            "observado": row.observado,
            "estado": row.estado,
            "id_circuito": row.id_circuito,
            "numero_lista": row.numero_lista,
            "organ": row.organ,
            "departamento": row.departamento
        })
    return votos

@router.get("/circuito/{id_circuito}")
def obtener_votos_por_circuito(id_circuito: int, db = Depends(get_db)):
    query = text("""
        SELECT v.id_voto, v.fecha_hora_emision, v.observado, v.estado,
               v.id_eleccion, v.numero_lista
        FROM voto v
        WHERE v.id_circuito = :id_circuito
        ORDER BY v.fecha_hora_emision
    """)
    result = db.execute(query, {"id_circuito": id_circuito})
    votos = []
    for row in result:
        votos.append({
            "id_voto": row.id_voto,
            "fecha_hora_emision": row.fecha_hora_emision,
            "observado": row.observado,
            "estado": row.estado,
            "id_eleccion": row.id_eleccion,
            "numero_lista": row.numero_lista
        })
    return votos

@router.post("/registrar")
def registrar_voto(voto_data: dict, db = Depends(get_db)):
    try:
        query = text("""
            INSERT INTO voto (fecha_hora_emision, observado, estado, id_eleccion, id_circuito, numero_lista)
            VALUES (:fecha_hora, :observado, :estado, :id_eleccion, :id_circuito, :numero_lista)
            RETURNING id_voto
        """)
        
        result = db.execute(query, {
            "fecha_hora": datetime.now(),
            "observado": voto_data.get("observado", False),
            "estado": voto_data.get("estado", "Válido"),
            "id_eleccion": voto_data["id_eleccion"],
            "id_circuito": voto_data["id_circuito"],
            "numero_lista": voto_data.get("numero_lista")
        })
        
        db.commit()
        new_id = result.fetchone()[0]
        return {"mensaje": "Voto registrado exitosamente", "id_voto": new_id}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al registrar voto: {str(e)}")
