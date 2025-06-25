from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.persona import router as persona_router
from app.database import Base, engine

app = FastAPI()

# CORS: permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend de Vite
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
