from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, DECIMAL, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config.database import Base
import enum

class TipoResiduo(str, enum.Enum):
    organico = "organico"
    plastico = "plastico"
    papel = "papel"
    vidrio = "vidrio"
    metal = "metal"
    electronico = "electronico"
    otros = "otros"

class EstadoReporte(str, enum.Enum):
    pendiente = "pendiente"
    en_proceso = "en_proceso"
    resuelto = "resuelto"
    rechazado = "rechazado"

class Prioridad(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    ubicacion = Column(String(255), nullable=False)
    latitud = Column(DECIMAL(10, 8), nullable=True)
    longitud = Column(DECIMAL(11, 8), nullable=True)
    tipo_residuo = Column(Enum(TipoResiduo), nullable=False)
    estado = Column(Enum(EstadoReporte), default=EstadoReporte.pendiente, nullable=False)
    prioridad = Column(Enum(Prioridad), default=Prioridad.media, nullable=False)
    imagen_url = Column(String(500), nullable=True)
    fecha_reporte = Column(DateTime(timezone=True), server_default=func.now())
    fecha_resolucion = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())