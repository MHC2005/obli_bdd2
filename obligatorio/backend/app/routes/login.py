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

    query = text("SELECT ci, password FROM persona WHERE ci = :ci")
    
    with engine.connect() as conn:
        result = conn.execute(query, {"ci": ci})
        row = result.fetchone()

        if not row or row.password != password:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        # Generar token JWT
        token = create_access_token({"ci": row.ci, "rol": "votante" if row.ci != 11111111 else "presidente"})

    return {"ci": row.ci, "token": token, "rol": "votante" if row.ci != 11111111 else "presidente"}
