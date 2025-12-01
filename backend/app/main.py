from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from .config.database import create_tables, test_connection
from .routes import (
    auth_router,
    users_router,
    reports_router,
    recycling_router,
    schedules_router
)

load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(
    title="Eco-Continental API",
    description="API para la gestión de residuos sólidos en Huancayo",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Evento de inicio
@app.on_event("startup")
async def startup_event():
    """Ejecutar al iniciar la aplicación"""
    print("🚀 Iniciando Eco-Continental API...")
    
    # Verificar conexión a la base de datos
    if test_connection():
        print("✅ Conexión a base de datos exitosa")
        # Crear tablas si no existen
        create_tables()
    else:
        print("❌ Error al conectar con la base de datos")

# Ruta raíz
@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Bienvenido a Eco-Continental API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

# Ruta de salud
@app.get("/health")
async def health_check():
    """Verificar estado de la API"""
    return {
        "status": "healthy",
        "database": "connected"
    }

# Incluir routers con prefijo API v1
api_v1_prefix = os.getenv("API_V1_PREFIX", "/api/v1")

app.include_router(auth_router, prefix=api_v1_prefix)
app.include_router(users_router, prefix=api_v1_prefix)
app.include_router(reports_router, prefix=api_v1_prefix)
app.include_router(recycling_router, prefix=api_v1_prefix)
app.include_router(schedules_router, prefix=api_v1_prefix)

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Error interno del servidor",
            "detail": str(exc) if os.getenv("DEBUG") == "True" else None
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )