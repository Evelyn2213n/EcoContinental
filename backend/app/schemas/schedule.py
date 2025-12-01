from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time
from ..models.schedule import DiaSemana, TipoRecoleccion, EstadoHorario

# Schema base
class ScheduleBase(BaseModel):
    zona: str = Field(..., min_length=3, max_length=100)
    distrito: str = Field(..., min_length=3, max_length=100)
    dia_semana: DiaSemana
    hora_inicio: time
    hora_fin: time
    tipo_recoleccion: TipoRecoleccion
    descripcion: Optional[str] = None

# Schema para crear horario
class ScheduleCreate(ScheduleBase):
    pass

# Schema para actualizar horario
class ScheduleUpdate(BaseModel):
    zona: Optional[str] = Field(None, min_length=3, max_length=100)
    distrito: Optional[str] = Field(None, min_length=3, max_length=100)
    dia_semana: Optional[DiaSemana] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    tipo_recoleccion: Optional[TipoRecoleccion] = None
    descripcion: Optional[str] = None
    estado: Optional[EstadoHorario] = None

# Schema de respuesta
class ScheduleResponse(ScheduleBase):
    id: int
    estado: EstadoHorario
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

