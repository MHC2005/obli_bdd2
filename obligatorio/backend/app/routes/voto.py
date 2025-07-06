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
✅ GET /votos/verificar/{ci}/{id_eleccion} - Verificar si una persona ya votó en una elección
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
               v.id_circuito, v.numero_lista, l.organ as nombre_lista, l.departamento
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
            "nombre_lista": row.nombre_lista,
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
        
        # Verificar si ya existe un voto para este circuito en esta elección
        # (Asumimos que cada circuito corresponde a una persona única)
        voto_existente_query = text("""
            SELECT id_voto FROM voto 
            WHERE id_circuito = :id_circuito AND id_eleccion = :id_eleccion
        """)
        voto_existente_result = db.execute(voto_existente_query, {
            "id_circuito": voto_data["id_circuito"], 
            "id_eleccion": voto_data["id_eleccion"]
        })
        if voto_existente_result.fetchone():
            raise HTTPException(
                status_code=400, 
                detail="Esta persona ya ha emitido su voto en esta elección. Solo se permite un voto por persona por elección."
            )
        
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

@router.get("/verificar/{ci}/{id_eleccion}")
def verificar_voto_existente(ci: int, id_eleccion: int, db = Depends(get_db)):
    """
    Verifica si una persona ya votó en una elección específica
    """
    try:
        # Buscar si ya existe un voto para esta persona en esta elección
        query = text("""
            SELECT v.id_voto, v.fecha_hora_emision, v.estado
            FROM voto v
            INNER JOIN ciudadano cd ON cd.id_circuito = v.id_circuito
            INNER JOIN persona p ON p.ci = cd.ci
            WHERE p.ci = :ci AND v.id_eleccion = :id_eleccion
            LIMIT 1
        """)
        result = db.execute(query, {"ci": ci, "id_eleccion": id_eleccion})
        voto_existente = result.fetchone()
        
        if voto_existente:
            return {
                "ya_voto": True,
                "id_voto": voto_existente.id_voto,
                "fecha_hora_emision": voto_existente.fecha_hora_emision,
                "estado": voto_existente.estado,
                "mensaje": "Esta persona ya ha emitido su voto en esta elección"
            }
        else:
            return {
                "ya_voto": False,
                "mensaje": "Esta persona puede votar en esta elección"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando voto: {str(e)}")

@router.get("/observados")
def obtener_votos_observados(db = Depends(get_db)):
    """
    Obtiene todos los votos marcados como observados que requieren autorización
    """
    try:
        query = text("""
            SELECT DISTINCT v.id_voto, v.fecha_hora_emision, v.observado, v.estado,
                   v.id_eleccion, v.id_circuito, v.numero_lista,
                   p.ci, p.nombre_completo, e.tipo as tipo_eleccion,
                   c.barrio, c.departamento
            FROM voto v
            INNER JOIN ciudadano cd ON cd.id_circuito = v.id_circuito
            INNER JOIN persona p ON p.ci = cd.ci
            INNER JOIN eleccion e ON v.id_eleccion = e.id_eleccion
            INNER JOIN circuito c ON v.id_circuito = c.id_circuito
            WHERE v.observado = TRUE AND v.estado = 'Observado'
            ORDER BY v.fecha_hora_emision DESC
        """)
        result = db.execute(query)
        votos_observados = []
        
        for row in result:
            votos_observados.append({
                "id_voto": row.id_voto,
                "fecha_hora_emision": row.fecha_hora_emision,
                "observado": row.observado,
                "estado": row.estado,
                "id_eleccion": row.id_eleccion,
                "id_circuito": row.id_circuito,
                "numero_lista": row.numero_lista,
                "ci": row.ci,
                "nombre_completo": row.nombre_completo,
                "tipo_eleccion": row.tipo_eleccion,
                "barrio": row.barrio,
                "departamento": row.departamento
            })
        
        return votos_observados
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo votos observados: {str(e)}")

@router.post("/autorizar/{id_voto}")
def autorizar_voto_observado(id_voto: int, accion: dict, db = Depends(get_db)):
    """
    Autoriza o rechaza un voto observado
    accion debe contener: {"decision": "aprobar" | "rechazar", "motivo": "texto opcional"}
    """
    try:
        # Verificar que el voto existe y está observado
        query_verificar = text("""
            SELECT id_voto, estado, observado 
            FROM voto 
            WHERE id_voto = :id_voto AND observado = TRUE
        """)
        result = db.execute(query_verificar, {"id_voto": id_voto})
        voto = result.fetchone()
        
        if not voto:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró voto observado con ID {id_voto}"
            )
        
        # Determinar el nuevo estado según la decisión
        decision = accion.get("decision")
        if decision == "aprobar":
            nuevo_estado = "Válido"
        elif decision == "rechazar":
            nuevo_estado = "Rechazado"
        else:
            raise HTTPException(
                status_code=400, 
                detail="La decisión debe ser 'aprobar' o 'rechazar'"
            )
        
        # Actualizar el voto
        query_actualizar = text("""
            UPDATE voto 
            SET estado = :nuevo_estado, observado = FALSE 
            WHERE id_voto = :id_voto
        """)
        db.execute(query_actualizar, {
            "nuevo_estado": nuevo_estado,
            "id_voto": id_voto
        })
        db.commit()
        
        return {
            "id_voto": id_voto,
            "decision": decision,
            "nuevo_estado": nuevo_estado,
            "motivo": accion.get("motivo", ""),
            "mensaje": f"Voto {id_voto} {decision}do exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error autorizando voto: {str(e)}")

@router.post("/marcar-observado")
def marcar_voto_observado(voto_data: dict, db = Depends(get_db)):
    """
    Registra un voto como observado cuando hay alguna irregularidad o consulta
    """
    try:
        # Validaciones básicas
        required_fields = ["numero_lista", "id_eleccion", "id_circuito", "motivo_observacion"]
        for field in required_fields:
            if field not in voto_data:
                raise HTTPException(status_code=400, detail=f"Campo requerido: {field}")
        
        # Verificar que no exista ya un voto para este circuito en esta elección
        voto_existente_query = text("""
            SELECT id_voto FROM voto 
            WHERE id_circuito = :id_circuito AND id_eleccion = :id_eleccion
        """)
        voto_existente_result = db.execute(voto_existente_query, {
            "id_circuito": voto_data["id_circuito"], 
            "id_eleccion": voto_data["id_eleccion"]
        })
        if voto_existente_result.fetchone():
            raise HTTPException(
                status_code=400, 
                detail="Esta persona ya ha emitido su voto en esta elección."
            )
        
        # Obtener el próximo ID disponible
        id_query = text("SELECT COALESCE(MAX(id_voto), 0) + 1 FROM voto")
        id_result = db.execute(id_query)
        next_id = id_result.fetchone()[0]
        
        # Insertar el voto observado
        query = text("""
            INSERT INTO voto (id_voto, fecha_hora_emision, observado, estado, id_eleccion, id_circuito, numero_lista)
            VALUES (:id_voto, :fecha_hora, :observado, :estado, :id_eleccion, :id_circuito, :numero_lista)
        """)
        
        db.execute(query, {
            "id_voto": next_id,
            "fecha_hora": datetime.now(),
            "observado": True,
            "estado": "Observado",
            "id_eleccion": voto_data["id_eleccion"],
            "id_circuito": voto_data["id_circuito"],
            "numero_lista": voto_data["numero_lista"]
        })
        db.commit()
        
        return {
            "id_voto": next_id,
            "mensaje": "Voto registrado como observado exitosamente",
            "motivo": voto_data["motivo_observacion"],
            "estado": "Observado",
            "requiere_autorizacion": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error registrando voto observado: {str(e)}")

@router.post("/crear-voto-observado-prueba")
def crear_voto_observado_prueba(db = Depends(get_db)):
    """
    Crea un voto observado de prueba para testing
    """
    try:
        # Obtener una elección activa
        eleccion_query = text("SELECT id_eleccion FROM eleccion LIMIT 1")
        eleccion_result = db.execute(eleccion_query)
        eleccion = eleccion_result.fetchone()
        
        if not eleccion:
            raise HTTPException(status_code=400, detail="No hay elecciones disponibles")
        
        # Buscar un circuito que NO haya votado en esta elección
        circuito_query = text("""
            SELECT c.id_circuito 
            FROM circuito c
            LEFT JOIN voto v ON c.id_circuito = v.id_circuito AND v.id_eleccion = :id_eleccion
            WHERE v.id_voto IS NULL
            LIMIT 1
        """)
        circuito_result = db.execute(circuito_query, {"id_eleccion": eleccion.id_eleccion})
        circuito = circuito_result.fetchone()
        
        if not circuito:
            # Si no hay circuitos disponibles, crear uno temporal
            # Obtener el próximo ID de circuito
            max_circuito_query = text("SELECT COALESCE(MAX(id_circuito), 0) + 1 FROM circuito")
            max_circuito_result = db.execute(max_circuito_query)
            nuevo_id_circuito = max_circuito_result.fetchone()[0]
            
            # Crear nuevo circuito temporal
            crear_circuito_query = text("""
                INSERT INTO circuito (id_circuito, barrio, departamento)
                VALUES (:id_circuito, 'Circuito Prueba', 'Montevideo')
            """)
            db.execute(crear_circuito_query, {"id_circuito": nuevo_id_circuito})
            
            # Crear persona asociada al circuito
            crear_persona_query = text("""
                INSERT INTO persona (ci, nombre_completo, password)
                VALUES (:ci, 'Votante Prueba', 'password')
            """)
            ci_prueba = 90000000 + nuevo_id_circuito  # CI único
            db.execute(crear_persona_query, {"ci": ci_prueba})
            
            # Crear ciudadano vinculado
            crear_ciudadano_query = text("""
                INSERT INTO ciudadano (ci, id_circuito)
                VALUES (:ci, :id_circuito)
            """)
            db.execute(crear_ciudadano_query, {
                "ci": ci_prueba,
                "id_circuito": nuevo_id_circuito
            })
            
            id_circuito_usar = nuevo_id_circuito
        else:
            id_circuito_usar = circuito.id_circuito
        
        # Obtener el próximo ID de voto
        id_query = text("SELECT COALESCE(MAX(id_voto), 0) + 1 FROM voto")
        next_id = db.execute(id_query).fetchone()[0]
        
        # Crear voto observado
        query = text("""
            INSERT INTO voto (id_voto, fecha_hora_emision, observado, estado, id_eleccion, id_circuito, numero_lista)
            VALUES (:id_voto, :fecha_hora, TRUE, 'Observado', :id_eleccion, :id_circuito, 101)
        """)
        
        db.execute(query, {
            "id_voto": next_id,
            "fecha_hora": datetime.now(),
            "id_eleccion": eleccion.id_eleccion,
            "id_circuito": id_circuito_usar
        })
        db.commit()
        
        return {
            "id_voto": next_id,
            "mensaje": "Voto observado de prueba creado exitosamente",
            "id_eleccion": eleccion.id_eleccion,
            "id_circuito": id_circuito_usar,
            "circuito_creado": circuito is None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creando voto de prueba: {str(e)}")

@router.delete("/limpiar-votos-prueba")
def limpiar_votos_prueba(db = Depends(get_db)):
    """
    Elimina todos los votos observados de prueba y circuitos temporales
    """
    try:
        # Eliminar votos observados de circuitos de prueba
        delete_votos_query = text("""
            DELETE FROM voto 
            WHERE id_circuito IN (
                SELECT id_circuito FROM circuito 
                WHERE barrio = 'Circuito Prueba'
            )
        """)
        votos_eliminados = db.execute(delete_votos_query)
        
        # Eliminar ciudadanos de circuitos de prueba
        delete_ciudadanos_query = text("""
            DELETE FROM ciudadano 
            WHERE id_circuito IN (
                SELECT id_circuito FROM circuito 
                WHERE barrio = 'Circuito Prueba'
            )
        """)
        ciudadanos_eliminados = db.execute(delete_ciudadanos_query)
        
        # Eliminar personas de prueba
        delete_personas_query = text("""
            DELETE FROM persona 
            WHERE ci >= 90000000 AND nombre_completo = 'Votante Prueba'
        """)
        personas_eliminadas = db.execute(delete_personas_query)
        
        # Eliminar circuitos de prueba
        delete_circuitos_query = text("""
            DELETE FROM circuito 
            WHERE barrio = 'Circuito Prueba'
        """)
        circuitos_eliminados = db.execute(delete_circuitos_query)
        
        db.commit()
        
        return {
            "mensaje": "Datos de prueba eliminados exitosamente",
            "votos_eliminados": votos_eliminados.rowcount,
            "ciudadanos_eliminados": ciudadanos_eliminados.rowcount,
            "personas_eliminadas": personas_eliminadas.rowcount,
            "circuitos_eliminados": circuitos_eliminados.rowcount
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error limpiando datos de prueba: {str(e)}")

@router.get("/diagnostico-duplicados")
def diagnostico_duplicados(db = Depends(get_db)):
    """
    Diagnóstico para revisar posibles duplicados en la base de datos
    """
    try:
        # Revisar si hay múltiples ciudadanos por circuito
        query_ciudadanos = text("""
            SELECT id_circuito, COUNT(*) as ciudadanos_count
            FROM ciudadano 
            GROUP BY id_circuito 
            HAVING COUNT(*) > 1
            ORDER BY ciudadanos_count DESC
        """)
        result_ciudadanos = db.execute(query_ciudadanos)
        circuitos_con_multiples_ciudadanos = []
        for row in result_ciudadanos:
            circuitos_con_multiples_ciudadanos.append({
                "id_circuito": row.id_circuito,
                "ciudadanos_count": row.ciudadanos_count
            })
        
        # Revisar votos observados con detalles
        query_votos = text("""
            SELECT v.id_voto, v.id_circuito, COUNT(*) as apariciones
            FROM voto v
            INNER JOIN ciudadano cd ON cd.id_circuito = v.id_circuito
            WHERE v.observado = TRUE AND v.estado = 'Observado'
            GROUP BY v.id_voto, v.id_circuito
            HAVING COUNT(*) > 1
        """)
        result_votos = db.execute(query_votos)
        votos_con_duplicados = []
        for row in result_votos:
            votos_con_duplicados.append({
                "id_voto": row.id_voto,
                "id_circuito": row.id_circuito,
                "apariciones": row.apariciones
            })
        
        return {
            "circuitos_con_multiples_ciudadanos": circuitos_con_multiples_ciudadanos,
            "votos_con_duplicados": votos_con_duplicados,
            "total_circuitos_problematicos": len(circuitos_con_multiples_ciudadanos),
            "total_votos_problematicos": len(votos_con_duplicados)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en diagnóstico: {str(e)}")
