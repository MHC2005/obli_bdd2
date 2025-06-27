from fastapi import APIRouter, Depends
from sqlalchemy import text
from ..database import engine

"""
ENDPOINTS DISPONIBLES EN PERSONAS:
✅ GET /personas/ - Listar todas las personas
✅ GET /personas/por-rol/{rol} - Filtrar por rol (ciudadano, candidato, miembro_mesa, agente_policial)
✅ GET /personas/con-roles - Listar personas con sus roles detectados dinámicamente
✅ GET /personas/candidatos/por-eleccion/{id_eleccion} - Candidatos en una elección específica
✅ GET /personas/miembros-mesa/por-circuito/{id_circuito} - Autoridades de mesa por circuito
✅ GET /personas/buscar?nombre=X&ci=Y&numero=Z - Búsqueda flexible por múltiples criterios
✅ GET /personas/estadisticas - Estadísticas generales de personas por rol
✅ GET /personas/{ci} - Obtener persona específica por CI
✅ GET /personas/{ci}/detalle-completo - Perfil completo con todos los roles de la persona
"""

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

@router.get("/por-rol/{rol}")
def obtener_personas_por_rol(rol: str, db = Depends(get_db)):
    rol_lower = rol.lower()
    
    if rol_lower == "ciudadano":
        query = text("""
            SELECT p.ci, p.nombre_completo, p.numero, p.serie,
                   c.fecha_nacimiento, c.id_circuito,
                   circ.barrio, circ.localidad, circ.departamento
            FROM persona p
            INNER JOIN ciudadano c ON p.ci = c.ci
            LEFT JOIN circuito circ ON c.id_circuito = circ.id_circuito
            ORDER BY p.nombre_completo
        """)
    elif rol_lower == "candidato":
        query = text("""
            SELECT p.ci, p.nombre_completo, p.numero, p.serie,
                   can.cargo_postulado
            FROM persona p
            INNER JOIN candidato can ON p.ci = can.ci
            ORDER BY p.nombre_completo
        """)
    elif rol_lower == "miembro_mesa":
        query = text("""
            SELECT p.ci, p.nombre_completo, p.numero, p.serie,
                   mm.organismo_estado
            FROM persona p
            INNER JOIN miembro_mesa mm ON p.ci = mm.ci
            ORDER BY p.nombre_completo
        """)
    elif rol_lower == "agente_policial":
        query = text("""
            SELECT p.ci, p.nombre_completo, p.numero, p.serie,
                   ap.comisaria, ap.id_establecimiento,
                   e.nombre as establecimiento_nombre
            FROM persona p
            INNER JOIN agente_policial ap ON p.ci = ap.ci
            LEFT JOIN establecimiento e ON ap.id_establecimiento = e.id_establecimiento
            ORDER BY p.nombre_completo
        """)
    else:
        return {"error": "Rol no válido. Use: ciudadano, candidato, miembro_mesa, agente_policial"}
    
    result = db.execute(query)
    personas = []
    for row in result:
        persona = {
            "ci": row.ci,
            "nombre_completo": row.nombre_completo,
            "numero": row.numero,
            "serie": row.serie
        }
        
        # Agregar campos específicos del rol (sin incluir "rol" como campo)
        if rol_lower == "ciudadano":
            persona.update({
                "fecha_nacimiento": row.fecha_nacimiento,
                "id_circuito": row.id_circuito,
                "barrio": row.barrio,
                "localidad": row.localidad,
                "departamento": row.departamento
            })
        elif rol_lower == "candidato":
            persona["cargo_postulado"] = row.cargo_postulado
        elif rol_lower == "miembro_mesa":
            persona["organismo_estado"] = row.organismo_estado
        elif rol_lower == "agente_policial":
            persona.update({
                "comisaria": row.comisaria,
                "id_establecimiento": row.id_establecimiento,
                "establecimiento_nombre": row.establecimiento_nombre
            })
            
        personas.append(persona)
    
    return personas

@router.get("/con-roles")
def listar_personas_con_roles(db = Depends(get_db)):
    query = text("""
        SELECT p.ci, p.nombre_completo, p.numero, p.serie,
               CASE 
                   WHEN c.ci IS NOT NULL THEN 'Ciudadano'
                   ELSE NULL
               END as es_ciudadano,
               CASE 
                   WHEN can.ci IS NOT NULL THEN 'Candidato'
                   ELSE NULL
               END as es_candidato,
               CASE 
                   WHEN mm.ci IS NOT NULL THEN 'Miembro_Mesa'
                   ELSE NULL
               END as es_miembro_mesa,
               CASE 
                   WHEN ap.ci IS NOT NULL THEN 'Agente_Policial'
                   ELSE NULL
               END as es_agente_policial,
               c.fecha_nacimiento,
               can.cargo_postulado,
               mm.organismo_estado,
               ap.comisaria
        FROM persona p
        LEFT JOIN ciudadano c ON p.ci = c.ci
        LEFT JOIN candidato can ON p.ci = can.ci
        LEFT JOIN miembro_mesa mm ON p.ci = mm.ci
        LEFT JOIN agente_policial ap ON p.ci = ap.ci
        ORDER BY p.nombre_completo
    """)
    result = db.execute(query)
    personas = []
    for row in result:
        roles = []
        if row.es_ciudadano:
            roles.append("Ciudadano")
        if row.es_candidato:
            roles.append("Candidato")
        if row.es_miembro_mesa:
            roles.append("Miembro_Mesa")
        if row.es_agente_policial:
            roles.append("Agente_Policial")
        
        persona = {
            "ci": row.ci,
            "nombre_completo": row.nombre_completo,
            "numero": row.numero,
            "serie": row.serie,
            "roles": roles if roles else ["Sin_Rol"]
        }
        
        # Agregar detalles específicos si tiene roles
        if row.es_ciudadano:
            persona["fecha_nacimiento"] = row.fecha_nacimiento
        if row.es_candidato:
            persona["cargo_postulado"] = row.cargo_postulado
        if row.es_miembro_mesa:
            persona["organismo_estado"] = row.organismo_estado
        if row.es_agente_policial:
            persona["comisaria"] = row.comisaria
            
        personas.append(persona)
    
    return personas

@router.get("/candidatos/por-eleccion/{id_eleccion}")
def obtener_candidatos_por_eleccion(id_eleccion: int, db = Depends(get_db)):
    query = text("""
        SELECT p.ci, p.nombre_completo, c.cargo_postulado,
               l.numero_lista, pp.nombre as partido_nombre
        FROM persona p
        INNER JOIN candidato c ON p.ci = c.ci
        INNER JOIN presentan pr ON c.ci = pr.ci
        LEFT JOIN lista l ON c.ci = l.ci
        LEFT JOIN partido_politico pp ON l.id_partido_politico = pp.id_partido_politico
        WHERE pr.id_eleccion = :id_eleccion
        ORDER BY c.cargo_postulado, p.nombre_completo
    """)
    result = db.execute(query, {"id_eleccion": id_eleccion})
    candidatos = []
    for row in result:
        candidatos.append({
            "ci": row.ci,
            "nombre_completo": row.nombre_completo,
            "cargo_postulado": row.cargo_postulado,
            "numero_lista": row.numero_lista,
            "partido_nombre": row.partido_nombre
        })
    return candidatos

@router.get("/miembros-mesa/por-circuito/{id_circuito}")
def obtener_miembros_mesa_por_circuito(id_circuito: int, db = Depends(get_db)):
    query = text("""
        SELECT p.ci, p.nombre_completo, mm.organismo_estado, i.cargo
        FROM persona p
        INNER JOIN miembro_mesa mm ON p.ci = mm.ci
        INNER JOIN integra i ON mm.ci = i.ci
        WHERE i.id_circuito = :id_circuito
        ORDER BY 
            CASE i.cargo 
                WHEN 'Presidente de Mesa' THEN 1
                WHEN 'Secretario de Mesa' THEN 2
                WHEN 'Vocal' THEN 3
                ELSE 4
            END,
            p.nombre_completo
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

@router.get("/buscar")
def buscar_personas(nombre: str = None, ci: int = None, numero: str = None, db = Depends(get_db)):
    if not any([nombre, ci, numero]):
        return {"error": "Debe proporcionar al menos un parámetro de búsqueda: nombre, ci o numero"}
    
    conditions = []
    params = {}
    
    if nombre:
        conditions.append("LOWER(nombre_completo) LIKE LOWER(:nombre)")
        params["nombre"] = f"%{nombre}%"
    
    if ci:
        conditions.append("ci = :ci")
        params["ci"] = ci
        
    if numero:
        conditions.append("numero = :numero")
        params["numero"] = numero
    
    where_clause = " AND ".join(conditions)
    
    query = text(f"""
        SELECT ci, nombre_completo, numero, serie
        FROM persona 
        WHERE {where_clause}
        ORDER BY nombre_completo
        LIMIT 50
    """)
    
    result = db.execute(query, params)
    personas = []
    for row in result:
        personas.append({
            "ci": row.ci,
            "nombre_completo": row.nombre_completo,
            "numero": row.numero,
            "serie": row.serie
        })
    return personas

@router.get("/estadisticas")
def obtener_estadisticas_personas(db = Depends(get_db)):
    query = text("""
        SELECT 
            COUNT(*) as total_personas,
            COUNT(DISTINCT c.ci) as total_ciudadanos,
            COUNT(DISTINCT can.ci) as total_candidatos,
            COUNT(DISTINCT mm.ci) as total_miembros_mesa,
            COUNT(DISTINCT ap.ci) as total_agentes_policiales
        FROM persona p
        LEFT JOIN ciudadano c ON p.ci = c.ci
        LEFT JOIN candidato can ON p.ci = can.ci
        LEFT JOIN miembro_mesa mm ON p.ci = mm.ci
        LEFT JOIN agente_policial ap ON p.ci = ap.ci
    """)
    result = db.execute(query)
    row = result.fetchone()
    
    return {
        "total_personas": row.total_personas,
        "total_ciudadanos": row.total_ciudadanos,
        "total_candidatos": row.total_candidatos,
        "total_miembros_mesa": row.total_miembros_mesa,
        "total_agentes_policiales": row.total_agentes_policiales,
        "personas_sin_rol": row.total_personas - (row.total_ciudadanos + row.total_candidatos + row.total_miembros_mesa + row.total_agentes_policiales)
    }

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

@router.get("/{ci}/detalle-completo")
def obtener_detalle_completo_persona(ci: int, db = Depends(get_db)):
    # Información básica de la persona
    query_persona = text("SELECT ci, nombre_completo, numero, serie FROM persona WHERE ci = :ci")
    result = db.execute(query_persona, {"ci": ci})
    persona_row = result.fetchone()
    
    if persona_row is None:
        return {"error": f"No se encontró persona con CI: {ci}"}
    
    persona = {
        "ci": persona_row.ci,
        "nombre_completo": persona_row.nombre_completo,
        "numero": persona_row.numero,
        "serie": persona_row.serie,
        "roles": []
    }
    
    # Verificar si es ciudadano
    query_ciudadano = text("""
        SELECT c.fecha_nacimiento, c.id_circuito,
               circ.barrio, circ.localidad, circ.departamento
        FROM ciudadano c
        LEFT JOIN circuito circ ON c.id_circuito = circ.id_circuito
        WHERE c.ci = :ci
    """)
    result = db.execute(query_ciudadano, {"ci": ci})
    ciudadano_row = result.fetchone()
    if ciudadano_row:
        persona["roles"].append({
            "tipo": "ciudadano",
            "fecha_nacimiento": ciudadano_row.fecha_nacimiento,
            "circuito": {
                "id": ciudadano_row.id_circuito,
                "barrio": ciudadano_row.barrio,
                "localidad": ciudadano_row.localidad,
                "departamento": ciudadano_row.departamento
            }
        })
    
    # Verificar si es candidato
    query_candidato = text("SELECT cargo_postulado FROM candidato WHERE ci = :ci")
    result = db.execute(query_candidato, {"ci": ci})
    candidato_row = result.fetchone()
    if candidato_row:
        persona["roles"].append({
            "tipo": "candidato",
            "cargo_postulado": candidato_row.cargo_postulado
        })
    
    # Verificar si es miembro de mesa
    query_miembro = text("SELECT organismo_estado FROM miembro_mesa WHERE ci = :ci")
    result = db.execute(query_miembro, {"ci": ci})
    miembro_row = result.fetchone()
    if miembro_row:
        persona["roles"].append({
            "tipo": "miembro_mesa",
            "organismo_estado": miembro_row.organismo_estado
        })
    
    # Verificar si es agente policial
    query_agente = text("""
        SELECT ap.comisaria, ap.id_establecimiento, e.nombre as establecimiento_nombre
        FROM agente_policial ap
        LEFT JOIN establecimiento e ON ap.id_establecimiento = e.id_establecimiento
        WHERE ap.ci = :ci
    """)
    result = db.execute(query_agente, {"ci": ci})
    agente_row = result.fetchone()
    if agente_row:
        persona["roles"].append({
            "tipo": "agente_policial",
            "comisaria": agente_row.comisaria,
            "establecimiento": {
                "id": agente_row.id_establecimiento,
                "nombre": agente_row.establecimiento_nombre
            }
        })
    
    return persona
