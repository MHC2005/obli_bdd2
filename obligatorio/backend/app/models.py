from sqlalchemy import Column, Integer, String
from .database import Base

class Persona(Base):
    __tablename__ = "persona"

    ci = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100))
    numero = Column(String(20))
    serie = Column(String(20))
