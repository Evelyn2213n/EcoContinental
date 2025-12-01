from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..config.database import get_db
from ..models.user import User, UserType
from ..models.schedule import Schedule, DiaSemana, EstadoHorario
from ..schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from ..middleware.auth import get_current_active_user, require_role

router = APIRouter(prefix="/schedules", tags=["Horarios de Recolección"])

@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_data: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserType.administrador]))
):
    """Crear nuevo horario (solo administradores)"""
    new_schedule = Schedule(**schedule_data.dict())
    
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    
    return new_schedule

@router.get("/", response_model=List[ScheduleResponse])
async def get_all_schedules(
    distrito: Optional[str] = None,
    zona: Optional[str] = None,
    dia_semana: Optional[DiaSemana] = None,
    db: Session = Depends(get_db)
):
    """Obtener todos los horarios"""
    query = db.query(Schedule).filter(Schedule.estado == EstadoHorario.activo)
    
    if distrito:
        query = query.filter(Schedule.distrito == distrito)
    if zona:
        query = query.filter(Schedule.zona == zona)
    if dia_semana:
        query = query.filter(Schedule.dia_semana == dia_semana)
    
    schedules = query.order_by(Schedule.distrito, Schedule.zona, Schedule.dia_semana).all()
    return schedules

@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule_by_id(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """Obtener horario por ID"""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horario no encontrado"
        )
    return schedule

@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserType.administrador]))
):
    """Actualizar horario (solo administradores)"""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horario no encontrado"
        )
    
    # Actualizar campos
    update_data = schedule_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(schedule, key, value)
    
    db.commit()
    db.refresh(schedule)
    
    return schedule

@router.delete("/{schedule_id}")
async def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserType.administrador]))
):
    """Eliminar horario (solo administradores)"""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horario no encontrado"
        )
    
    db.delete(schedule)
    db.commit()
    
    return {"message": "Horario eliminado exitosamente"}