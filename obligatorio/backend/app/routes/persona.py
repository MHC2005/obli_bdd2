from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.auth import create_access_token
from pydantic import BaseModel
from sqlalchemy import text

router = APIRouter()

class LoginRequest(BaseModel):
    ci: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()

    user = db.execute(
        text("SELECT * FROM persona WHERE ci = :ci AND serie = :password"),
        {"ci": data.ci, "password": data.password}
    ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    rol = "presidente" if user["ci"] == "11111111" else "votante"
    token = create_access_token({"ci": user["ci"], "rol": rol})

    return {"token": token, "ci": user["ci"], "rol": rol}

@router.options("/login")
def options_login():
    return {}
