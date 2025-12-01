from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..config.database import get_db
from ..models.user import User, UserType
from ..models.report import Report, EstadoReporte
from ..schemas.report import ReportCreate, ReportUpdate, ReportResponse, ReportWithUser, ReportStatistics
from ..middleware.auth import get_current_active_user, require_role

router = APIRouter(prefix="/reports", tags=["Reportes"])

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ReportCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nuevo reporte"""
    new_report = Report(
        user_id=current_user.id,
        titulo=report_data.titulo,
        descripcion=report_data.descripcion,
        ubicacion=report_data.ubicacion,
        latitud=report_data.latitud,
        longitud=report_data.longitud,
        tipo_residuo=report_data.tipo_residuo,
        prioridad=report_data.prioridad,
        imagen_url=report_data.imagen_url
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return new_report

@router.get("/", response_model=List[ReportWithUser])
async def get_all_reports(
    estado: Optional[EstadoReporte] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener todos los reportes"""
    query = db.query(
        Report,
        User.nombre.label('user_nombre'),
        User.apellido.label('user_apellido'),
        User.email.label('user_email')
    ).join(User, Report.user_id == User.id)
    
    if estado:
        query = query.filter(Report.estado == estado)
    
    results = query.order_by(Report.fecha_reporte.desc()).all()
    
    reports = []
    for report, user_nombre, user_apellido, user_email in results:
        report_dict = {
            **report.__dict__,
            'user_nombre': user_nombre,
            'user_apellido': user_apellido,
            'user_email': user_email
        }
        reports.append(report_dict)
    
    return reports

@router.get("/my-reports", response_model=List[ReportResponse])
async def get_my_reports(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener reportes del usuario actual"""
    reports = db.query(Report).filter(Report.user_id == current_user.id).order_by(Report.fecha_reporte.desc()).all()
    return reports

@router.get("/statistics", response_model=ReportStatistics)
async def get_report_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserType.administrador]))
):
    """Obtener estadísticas de reportes (solo administradores)"""
    total = db.query(func.count(Report.id)).scalar()
    pendiente = db.query(func.count(Report.id)).filter(Report.estado == EstadoReporte.pendiente).scalar()
    en_proceso = db.query(func.count(Report.id)).filter(Report.estado == EstadoReporte.en_proceso).scalar()
    resuelto = db.query(func.count(Report.id)).filter(Report.estado == EstadoReporte.resuelto).scalar()
    rechazado = db.query(func.count(Report.id)).filter(Report.estado == EstadoReporte.rechazado).scalar()
    
    return {
        "total": total,
        "pendiente": pendiente,
        "en_proceso": en_proceso,
        "resuelto": resuelto,
        "rechazado": rechazado
    }

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report_by_id(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener reporte por ID"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado"
        )
    return report

@router.put("/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar reporte"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado"
        )
    
    # Verificar permisos
    if report.user_id != current_user.id and current_user.tipo_usuario != UserType.administrador:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar este reporte"
        )
    
    # Actualizar campos
    if report_data.titulo:
        report.titulo = report_data.titulo
    if report_data.descripcion:
        report.descripcion = report_data.descripcion
    if report_data.ubicacion:
        report.ubicacion = report_data.ubicacion
    if report_data.tipo_residuo:
        report.tipo_residuo = report_data.tipo_residuo
    if report_data.prioridad:
        report.prioridad = report_data.prioridad
    if report_data.estado:
        report.estado = report_data.estado
        if report_data.estado == EstadoReporte.resuelto:
            from datetime import datetime
            report.fecha_resolucion = datetime.utcnow()
    
    db.commit()
    db.refresh(report)
    
    return report

@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar reporte"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado"
        )
    
    # Verificar permisos
    if report.user_id != current_user.id and current_user.tipo_usuario != UserType.administrador:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para eliminar este reporte"
        )
    
    db.delete(report)
    db.commit()
    
    return {"message": "Reporte eliminado exitosamente"}