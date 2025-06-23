from sqlalchemy import Column, Integer, String
from .database import Base

class Persona(Base):
    __tablename__ = "persona"

    CI = Column(Integer, primary_key=True, index=True)
    Nombre_Completo = Column(String(100))
    Numero = Column(String(20))
    Serie = Column(String(20))
