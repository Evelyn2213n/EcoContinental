from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from ..models.report import TipoResiduo, EstadoReporte, Prioridad

# Schema base
class ReportBase(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=200)
    descripcion: str = Field(..., min_length=10)
    ubicacion: str = Field(..., min_length=5, max_length=255)
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    tipo_residuo: TipoResiduo
    prioridad: Optional[Prioridad] = Prioridad.media

# Schema para crear reporte
class ReportCreate(ReportBase):
    imagen_url: Optional[str] = Field(None, max_length=500)

# Schema para actualizar reporte
class ReportUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=5, max_length=200)
    descripcion: Optional[str] = Field(None, min_length=10)
    ubicacion: Optional[str] = Field(None, min_length=5, max_length=255)
    tipo_residuo: Optional[TipoResiduo] = None
    prioridad: Optional[Prioridad] = None
    estado: Optional[EstadoReporte] = None

# Schema de respuesta
class ReportResponse(ReportBase):
    id: int
    user_id: int
    estado: EstadoReporte
    imagen_url: Optional[str]
    fecha_reporte: datetime
    fecha_resolucion: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema con información del usuario
class ReportWithUser(ReportResponse):
    user_nombre: Optional[str] = None
    user_apellido: Optional[str] = None
    user_email: Optional[str] = None

# Schema para estadísticas
class ReportStatistics(BaseModel):
    total: int
    pendiente: int
    en_proceso: int
    resuelto: int
    rechazado: int