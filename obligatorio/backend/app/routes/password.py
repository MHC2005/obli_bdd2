from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from app.database import engine
from app.password_utils import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])

def get_db():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@router.post("/cambiar-password")
async def cambiar_password(data: dict, db = Depends(get_db)):
    """
    Permite cambiar la contraseña de un usuario
    """
    ci = data.get("ci")
    password_actual = data.get("password_actual")
    password_nueva = data.get("password_nueva")
    
    if not ci or not password_actual or not password_nueva:
        raise HTTPException(
            status_code=400, 
            detail="CI, contraseña actual y nueva contraseña son requeridos"
        )
    
    if len(password_nueva) < 3:
        raise HTTPException(
            status_code=400, 
            detail="La nueva contraseña debe tener al menos 3 caracteres"
        )
    
    try:
        # Verificar que el usuario existe y la contraseña actual es correcta
        query_verificar = text("""
            SELECT password FROM persona WHERE ci = :ci
        """)
        result = db.execute(query_verificar, {"ci": ci})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar contraseña actual
        if not verify_password(password_actual, row.password):
            raise HTTPException(status_code=401, detail="Contraseña actual incorrecta")
        
        # Hashear nueva contraseña
        password_hasheada = hash_password(password_nueva)
        
        # Actualizar en la base de datos
        query_update = text("""
            UPDATE persona 
            SET password = :password_nueva 
            WHERE ci = :ci
        """)
        
        db.execute(query_update, {
            "password_nueva": password_hasheada,
            "ci": ci
        })
        db.commit()
        
        return {
            "mensaje": "Contraseña cambiada exitosamente",
            "ci": ci
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error cambiando contraseña: {str(e)}")

@router.post("/reset-password-admin")
async def reset_password_admin(data: dict, db = Depends(get_db)):
    """
    Permite al administrador resetear la contraseña de cualquier usuario
    Solo disponible para el presidente de mesa (CI 11111111)
    """
    ci_admin = data.get("ci_admin")
    ci_usuario = data.get("ci_usuario")
    password_nueva = data.get("password_nueva")
    
    if not ci_admin or not ci_usuario or not password_nueva:
        raise HTTPException(
            status_code=400, 
            detail="CI admin, CI usuario y nueva contraseña son requeridos"
        )
    
    # Verificar que quien hace el reset es el presidente
    if ci_admin != 11111111:
        raise HTTPException(
            status_code=403, 
            detail="Solo el presidente de mesa puede resetear contraseñas"
        )
    
    try:
        # Verificar que el usuario existe
        query_verificar = text("""
            SELECT ci FROM persona WHERE ci = :ci
        """)
        result = db.execute(query_verificar, {"ci": ci_usuario})
        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Hashear nueva contraseña
        password_hasheada = hash_password(password_nueva)
        
        # Actualizar en la base de datos
        query_update = text("""
            UPDATE persona 
            SET password = :password_nueva 
            WHERE ci = :ci
        """)
        
        db.execute(query_update, {
            "password_nueva": password_hasheada,
            "ci": ci_usuario
        })
        db.commit()
        
        return {
            "mensaje": f"Contraseña reseteada exitosamente para usuario {ci_usuario}",
            "ci_usuario": ci_usuario,
            "resetear_por": ci_admin
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error reseteando contraseña: {str(e)}")
