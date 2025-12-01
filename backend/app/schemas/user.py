from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from ..models.user import UserType, UserStatus

# Schema base
class UserBase(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=255)

# Schema para crear usuario
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    tipo_usuario: Optional[UserType] = UserType.ciudadano

# Schema para actualizar usuario
class UserUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=255)

# Schema para cambiar contraseña
class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)

# Schema de respuesta
class UserResponse(UserBase):
    id: int
    tipo_usuario: UserType
    estado: UserStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema para token
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None