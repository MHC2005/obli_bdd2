from fastapi import FastAPI
from app.routes.persona import router as persona_router  # suponiendo que así tenés tus rutas
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

app = FastAPI()

# Crear las tablas
Base.metadata.create_all(bind=engine)

# CORS (opcional, pero útil para desarrollo frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raíz para probar si está vivo el backend
@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente"}

# Registrar rutas
app.include_router(persona_router)
