from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, DECIMAL, Time
from sqlalchemy.sql import func
from ..config.database import Base
import enum

class EstadoPunto(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
    mantenimiento = "mantenimiento"

class RecyclingPoint(Base):
    __tablename__ = "recycling_points"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    direccion = Column(String(255), nullable=False)
    distrito = Column(String(100), nullable=False, index=True)
    latitud = Column(DECIMAL(10, 8), nullable=False)
    longitud = Column(DECIMAL(11, 8), nullable=False)
    tipo_materiales = Column(String(255), nullable=False)
    horario_apertura = Column(Time, nullable=True)
    horario_cierre = Column(Time, nullable=True)
    telefono = Column(String(20), nullable=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(Enum(EstadoPunto), default=EstadoPunto.activo, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())