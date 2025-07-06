from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.persona import router as persona_router
from app.routes.eleccion import router as eleccion_router
from app.routes.voto import router as voto_router
from app.routes.circuito import router as circuito_router
from app.routes.partido import router as partido_router
from app.routes.password import router as password_router
from app.database import Base, engine
from app.routes.login import router as login_router

app = FastAPI()

# CORS: permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Frontend de Vite (puertos alternativos)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

# Ruta raíz para verificar que el backend está vivo
@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente"}

# Registrar las rutas
app.include_router(persona_router)
app.include_router(eleccion_router)
app.include_router(voto_router)
app.include_router(circuito_router)
app.include_router(partido_router)
app.include_router(password_router)
app.include_router(login_router)

