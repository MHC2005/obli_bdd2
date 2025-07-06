try:
    from passlib.context import CryptContext
    PASSLIB_AVAILABLE = True
except ImportError:
    PASSLIB_AVAILABLE = False
    print("Warning: passlib no está instalado. Instale con: pip install passlib[bcrypt]")

import os

if PASSLIB_AVAILABLE:
    # Configurar el contexto de encriptación
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt
    """
    if not PASSLIB_AVAILABLE:
        raise ImportError("passlib no está disponible. Instale con: pip install passlib[bcrypt]")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña plana coincide con el hash
    """
    if not PASSLIB_AVAILABLE:
        # Fallback a comparación simple si passlib no está disponible
        return plain_password == hashed_password
    
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Error verificando contraseña: {e}")
        # Fallback a comparación simple
        return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """
    Alias para hash_password - para compatibilidad
    """
    return hash_password(password)
