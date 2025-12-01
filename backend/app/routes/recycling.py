from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, literal
from typing import List, Optional
from ..config.database import get_db
from ..models.user import User, UserType
from ..models.recycling_point import RecyclingPoint, EstadoPunto
from ..schemas.recycling_point import RecyclingPointCreate, RecyclingPointUpdate, RecyclingPointResponse, RecyclingPointNearby
from ..middleware.auth import get_current_active_user, require_role

router = APIRouter(prefix="/recycling-points", tags=["Puntos de Reciclaje"])

@router.post("/", response_model=RecyclingPointResponse, status_code=status.HTTP_201_CREATED)
async def create_recycling_point(
    point_data: RecyclingPointCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserType.administrador]))
):
    """Crear nuevo punto de reciclaje (solo administradores)"""
    new_point = RecyclingPoint(**point_data.dict())
    
    db.add(new_point)
    db.commit()
    db.refresh(new_point)
    
    return new_point

@router.get("/", response_model=List[RecyclingPointResponse])
async def get_all_recycling_points(
    distrito: Optional[str] = None,
    estado: Optional[EstadoPunto] = None,
    db: Session = Depends(get_db)
):
    """Obtener todos los puntos de reciclaje"""
    query = db.query(RecyclingPoint)
    
    if distrito:
        query = query.filter(RecyclingPoint.distrito == distrito)
    if estado:
        query = query.filter(RecyclingPoint.estado == estado)
    else:
        query = query.filter(RecyclingPoint.estado == EstadoPunto.activo)
    
    points = query.order_by(RecyclingPoint.nombre).all()
    return points

@router.get("/nearby", response_model=List[RecyclingPointNearby])
async def get_nearby_recycling_points(
    lat: float,
    lon: float,
    radius_km: float = 5.0,
    db: Session = Depends(get_db)
):
    """Obtener puntos de reciclaje cercanos usando fórmula de Haversine"""
    # Fórmula de Haversine para calcular distancia
    points = db.query(
        RecyclingPoint,
        (
            6371 * func.acos(
                func.cos(func.radians(literal(lat))) * 
                func.cos(func.radians(RecyclingPoint.latitud)) * 
                func.cos(func.radians(RecyclingPoint.longitud) - func.radians(literal(lon))) + 
                func.sin(func.radians(literal(lat))) * 
                func.sin(func.radians(RecyclingPoint.latitud))
            )
        ).label('distancia')
    ).filter(RecyclingPoint.estado == EstadoPunto.activo).all()
    
    # Filtrar por radio y ordenar
    nearby_points = []
    for point, distancia in points:
        if distancia <= radius_km:
            point_dict = {
                **point.__dict__,
                'distancia': round(distancia, 2)
            }
            nearby_points.append(point_dict)
    
    nearby_points.sort(key=lambda x: x['distancia'])
    return nearby_points

@router.get("/{point_id}", response_model=RecyclingPointResponse)
async def get_recycling_point_by_id(
    point_id: int,
    db: Session = Depends(get_db)
):
    """Obtener punto de reciclaje por ID"""
    point = db.query(RecyclingPoint).filter(RecyclingPoint.id == point_id).first()
    if not point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de reciclaje no encontrado"
        )
    return point

@router.put("/{point_id}", response_model=RecyclingPointResponse)
async def update_recycling_point(
    point_id: int,
    point_data: RecyclingPointUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserType.administrador]))
):
    """Actualizar punto de reciclaje (solo administradores)"""
    point = db.query(RecyclingPoint).filter(RecyclingPoint.id == point_id).first()
    if not point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de reciclaje no encontrado"
        )
    
    # Actualizar campos
    update_data = point_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(point, key, value)
    
    db.commit()
    db.refresh(point)
    
    return point

@router.delete("/{point_id}")
async def delete_recycling_point(
    point_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserType.administrador]))
):
    """Eliminar punto de reciclaje (solo administradores)"""
    point = db.query(RecyclingPoint).filter(RecyclingPoint.id == point_id).first()
    if not point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de reciclaje no encontrado"
        )
    
    db.delete(point)
    db.commit()
    
    return {"message": "Punto de reciclaje eliminado exitosamente"}