from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time
from decimal import Decimal
from ..models.recycling_point import EstadoPunto

# Schema base
class RecyclingPointBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=200)
    direccion: str = Field(..., min_length=5, max_length=255)
    distrito: str = Field(..., min_length=3, max_length=100)
    latitud: Decimal
    longitud: Decimal
    tipo_materiales: str = Field(..., min_length=3, max_length=255)
    horario_apertura: Optional[time] = None
    horario_cierre: Optional[time] = None
    telefono: Optional[str] = Field(None, max_length=20)
    descripcion: Optional[str] = None

# Schema para crear punto
class RecyclingPointCreate(RecyclingPointBase):
    pass

# Schema para actualizar punto
class RecyclingPointUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    direccion: Optional[str] = Field(None, min_length=5, max_length=255)
    distrito: Optional[str] = Field(None, min_length=3, max_length=100)
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    tipo_materiales: Optional[str] = Field(None, min_length=3, max_length=255)
    horario_apertura: Optional[time] = None
    horario_cierre: Optional[time] = None
    telefono: Optional[str] = Field(None, max_length=20)
    descripcion: Optional[str] = None
    estado: Optional[EstadoPunto] = None

# Schema de respuesta
class RecyclingPointResponse(RecyclingPointBase):
    id: int
    estado: EstadoPunto
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema para puntos cercanos
class RecyclingPointNearby(RecyclingPointResponse):
    distancia: Optional[float] = None