#!/usr/bin/env python3
"""
Script para hashear las contraseñas existentes en la base de datos
Ejecutar una sola vez después de instalar las dependencias
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine
from app.password_utils import hash_password

def hashear_contraseñas_existentes():
    """
    Hashea todas las contraseñas que están en texto plano en la base de datos
    """
    try:
        with engine.connect() as conn:
            # Obtener todas las personas con contraseñas en texto plano
            query_select = text("""
                SELECT ci, password 
                FROM persona 
                WHERE password IS NOT NULL 
                AND password != ''
                AND LENGTH(password) < 50  -- Las contraseñas hasheadas son más largas
            """)
            
            result = conn.execute(query_select)
            personas = result.fetchall()
            
            print(f"Encontradas {len(personas)} personas con contraseñas en texto plano")
            
            # Hashear cada contraseña
            for persona in personas:
                ci = persona.ci
                password_plain = persona.password
                password_hashed = hash_password(password_plain)
                
                # Actualizar en la base de datos
                query_update = text("""
                    UPDATE persona 
                    SET password = :password_hashed 
                    WHERE ci = :ci
                """)
                
                conn.execute(query_update, {
                    "password_hashed": password_hashed,
                    "ci": ci
                })
                
                print(f"✅ Contraseña hasheada para usuario CI: {ci}")
            
            # Confirmar cambios
            conn.commit()
            print(f"\n🎉 {len(personas)} contraseñas hasheadas exitosamente!")
            
    except Exception as e:
        print(f"❌ Error hasheando contraseñas: {str(e)}")
        return False
    
    return True

def verificar_hasheo():
    """
    Verifica que las contraseñas fueron hasheadas correctamente
    """
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT ci, password, LENGTH(password) as password_length
                FROM persona 
                WHERE password IS NOT NULL 
                ORDER BY ci
            """)
            
            result = conn.execute(query)
            personas = result.fetchall()
            
            print("\n📊 Estado de las contraseñas:")
            print("CI\t\tLongitud\tHasheada")
            print("-" * 40)
            
            for persona in personas:
                es_hasheada = len(persona.password) >= 50  # bcrypt genera hashes de ~60 caracteres
                estado = "✅ Sí" if es_hasheada else "❌ No"
                print(f"{persona.ci}\t{persona.password_length}\t\t{estado}")
                
    except Exception as e:
        print(f"❌ Error verificando hasheo: {str(e)}")

if __name__ == "__main__":
    print("🔐 Iniciando proceso de hasheo de contraseñas...")
    
    # Hashear contraseñas
    if hashear_contraseñas_existentes():
        # Verificar resultado
        verificar_hasheo()
    else:
        print("❌ El proceso de hasheo falló")
        sys.exit(1)
