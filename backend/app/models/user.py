from sqlalchemy import Column, Integer, String, Enum, DateTime, Text
from sqlalchemy.sql import func
from ..config.database import Base
import enum

class UserType(str, enum.Enum):
    ciudadano = "ciudadano"
    reciclador = "reciclador"
    administrador = "administrador"

class UserStatus(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)
    tipo_usuario = Column(Enum(UserType), default=UserType.ciudadano, nullable=False)
    estado = Column(Enum(UserStatus), default=UserStatus.activo, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())