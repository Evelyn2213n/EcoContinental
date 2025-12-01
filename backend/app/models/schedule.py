from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, Time
from sqlalchemy.sql import func
from ..config.database import Base
import enum

class DiaSemana(str, enum.Enum):
    lunes = "lunes"
    martes = "martes"
    miercoles = "miercoles"
    jueves = "jueves"
    viernes = "viernes"
    sabado = "sabado"
    domingo = "domingo"

class TipoRecoleccion(str, enum.Enum):
    residuos_comunes = "residuos_comunes"
    reciclables = "reciclables"
    organicos = "organicos"
    especiales = "especiales"

class EstadoHorario(str, enum.Enum):
    activo = "activo"
    suspendido = "suspendido"

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    zona = Column(String(100), nullable=False, index=True)
    distrito = Column(String(100), nullable=False, index=True)
    dia_semana = Column(Enum(DiaSemana), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    tipo_recoleccion = Column(Enum(TipoRecoleccion), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(Enum(EstadoHorario), default=EstadoHorario.activo, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


