from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import text
from app.database import engine
from app.auth import create_access_token

# Importar password_utils solo si está disponible
try:
    from app.password_utils import verify_password
    PASSWORD_UTILS_AVAILABLE = True
except ImportError:
    PASSWORD_UTILS_AVAILABLE = False
    print("Warning: password_utils no disponible, usando verificación de texto plano")

router = APIRouter()

def get_db():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@router.post("/login")
async def login_user(request: Request):
    try:
        data = await request.json()
        ci = data.get("ci")
        password = data.get("password")

        print(f"Login attempt for CI: {ci}")  # Debug

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

            if not row:
                print(f"User not found: {ci}")  # Debug
                raise HTTPException(status_code=401, detail="Credenciales inválidas")
            
            print(f"User found: {row.nombre_completo}")  # Debug
            
            # Verificar contraseña (soporta tanto hasheadas como texto plano)
            password_valida = False
            
            try:
                if PASSWORD_UTILS_AVAILABLE and row.password and row.password.startswith('$2b$'):
                    # Contraseña hasheada con bcrypt
                    print("Verifying hashed password")  # Debug
                    password_valida = verify_password(password, row.password)
                else:
                    # Contraseña en texto plano (fallback)
                    print("Verifying plain text password")  # Debug
                    password_valida = (password == row.password)
            except Exception as e:
                print(f"Error verificando contraseña: {e}")
                # Fallback a texto plano
                password_valida = (password == row.password)
            
            if not password_valida:
                print(f"Invalid password for user: {ci}")  # Debug
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            # Determinar rol
            rol = "presidente" if row.ci == 11111111 else "votante"
            print(f"User role: {rol}")  # Debug
            
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

            print(f"Login successful for: {ci}")  # Debug
            return user_data
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/debug-users")
async def debug_users():
    """
    Endpoint temporal para debug - mostrar usuarios disponibles
    """
    try:
        query = text("""
            SELECT p.ci, p.nombre_completo, 
                   CASE 
                       WHEN p.password IS NULL THEN 'NULL'
                       WHEN p.password = '' THEN 'EMPTY'
                       WHEN p.password LIKE '$2b$%' THEN 'HASHED'
                       ELSE 'PLAIN_TEXT'
                   END as password_type,
                   LENGTH(p.password) as password_length
            FROM persona p
            ORDER BY p.ci
        """)
        
        with engine.connect() as conn:
            result = conn.execute(query)
            users = []
            for row in result:
                users.append({
                    "ci": row.ci,
                    "nombre_completo": row.nombre_completo,
                    "password_type": row.password_type,
                    "password_length": row.password_length
                })
            
            return {
                "total_users": len(users),
                "users": users,
                "password_utils_available": PASSWORD_UTILS_AVAILABLE
            }
            
    except Exception as e:
        return {"error": str(e)}
