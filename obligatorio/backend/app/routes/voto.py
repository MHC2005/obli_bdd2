from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from ..database import engine
from datetime import datetime

"""
ENDPOINTS DISPONIBLES EN VOTOS:
✅ GET /votos/ - Listar todos los votos ordenados por fecha
✅ GET /votos/eleccion/{id_eleccion} - Votos de una elección específica con info de listas
✅ GET /votos/circuito/{id_circuito} - Votos de un circuito específico
✅ GET /votos/listas - Obtener todas las listas electorales disponibles
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

@router.get("/listas")
def obtener_listas_electorales(db = Depends(get_db)):
    query = text("""
        SELECT l.numero_lista, l.organ, l.departamento,
               p.nombre_completo as candidato_nombre,
               pp.nombre as partido_nombre
        FROM lista l
        LEFT JOIN candidato c ON l.ci = c.ci
        LEFT JOIN persona p ON c.ci = p.ci
        LEFT JOIN partido_politico pp ON l.id_partido_politico = pp.id_partido_politico
        ORDER BY l.numero_lista
    """)
    result = db.execute(query)
    listas = []
    for row in result:
        listas.append({
            "numero_lista": row.numero_lista,
            "organ": row.organ,
            "departamento": row.departamento,
            "candidato_nombre": row.candidato_nombre,
            "partido_nombre": row.partido_nombre
        })
    return listas

@router.post("/registrar")
def registrar_voto(voto_data: dict, db = Depends(get_db)):
    try:
        print(f"Datos recibidos para voto: {voto_data}")  # Debug
        
        # Validar campos requeridos
        if not voto_data.get("numero_lista"):
            raise HTTPException(status_code=400, detail="numero_lista es requerido")
        if not voto_data.get("id_eleccion"):
            raise HTTPException(status_code=400, detail="id_eleccion es requerido")
        if not voto_data.get("id_circuito"):
            raise HTTPException(status_code=400, detail="id_circuito es requerido")
        
        # Validar que la lista existe
        lista_query = text("SELECT numero_lista FROM lista WHERE numero_lista = :numero_lista")
        lista_result = db.execute(lista_query, {"numero_lista": voto_data.get("numero_lista")})
        if not lista_result.fetchone():
            # Obtener listas disponibles para mostrar en el error
            listas_query = text("SELECT numero_lista FROM lista ORDER BY numero_lista")
            listas_result = db.execute(listas_query)
            listas_disponibles = [str(row.numero_lista) for row in listas_result]
            raise HTTPException(
                status_code=400, 
                detail=f"La lista {voto_data.get('numero_lista')} no existe. Listas disponibles: {', '.join(listas_disponibles)}"
            )
        
        # Validar que la elección existe
        eleccion_query = text("SELECT id_eleccion FROM eleccion WHERE id_eleccion = :id_eleccion")
        eleccion_result = db.execute(eleccion_query, {"id_eleccion": voto_data["id_eleccion"]})
        if not eleccion_result.fetchone():
            raise HTTPException(status_code=400, detail=f"La elección {voto_data['id_eleccion']} no existe")
        
        # Validar que el circuito existe
        circuito_query = text("SELECT id_circuito FROM circuito WHERE id_circuito = :id_circuito")
        circuito_result = db.execute(circuito_query, {"id_circuito": voto_data["id_circuito"]})
        if not circuito_result.fetchone():
            raise HTTPException(status_code=400, detail=f"El circuito {voto_data['id_circuito']} no existe")
        
        # Primero obtenemos el próximo ID disponible
        id_query = text("SELECT COALESCE(MAX(id_voto), 0) + 1 FROM voto")
        id_result = db.execute(id_query)
        next_id = id_result.fetchone()[0]
        
        # Ahora insertamos el voto con el ID generado
        query = text("""
            INSERT INTO voto (id_voto, fecha_hora_emision, observado, estado, id_eleccion, id_circuito, numero_lista)
            VALUES (:id_voto, :fecha_hora, :observado, :estado, :id_eleccion, :id_circuito, :numero_lista)
        """)
        
        db.execute(query, {
            "id_voto": next_id,
            "fecha_hora": datetime.now(),
            "observado": voto_data.get("observado", False),
            "estado": voto_data.get("estado", "Válido"),
            "id_eleccion": voto_data["id_eleccion"],
            "id_circuito": voto_data["id_circuito"],
            "numero_lista": voto_data.get("numero_lista")
        })
        
        db.commit()
        print(f"Voto registrado exitosamente con ID: {next_id}")  # Debug
        return {"mensaje": "Voto registrado exitosamente", "id_voto": next_id}
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"Error en registrar_voto: {str(e)}")  # Debug
        raise HTTPException(status_code=400, detail=f"Error al registrar voto: {str(e)}")
