from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import text
from app.database import engine
from app.auth import create_access_token

router = APIRouter()

def get_db():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@router.post("/login")
async def login_user(request: Request):
    data = await request.json()
    ci = data.get("ci")
    password = data.get("password")

    if not ci or not password:
        raise HTTPException(status_code=400, detail="CI y contraseña requeridos")

    # Obtener información completa del usuario
    query = text("""
        SELECT p.ci, p.password, p.nombre_completo,
               c.id_circuito, circ.barrio, circ.departamento
        FROM persona p
        LEFT JOIN ciudadano c ON p.ci = c.ci
        LEFT JOIN circuito circ ON c.id_circuito = circ.id_circuito
        WHERE p.ci = :ci
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"ci": ci})
        row = result.fetchone()

        if not row or row.password != password:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        # Determinar rol
        rol = "presidente" if row.ci == 11111111 else "votante"
        
        # Generar token JWT
        token = create_access_token({"ci": row.ci, "rol": rol})
        
        # Datos de respuesta
        user_data = {
            "ci": row.ci,
            "token": token,
            "rol": rol,
            "nombre_completo": row.nombre_completo,
            "id_circuito": row.id_circuito,
            "barrio": row.barrio,
            "departamento": row.departamento
        }

    return user_data
