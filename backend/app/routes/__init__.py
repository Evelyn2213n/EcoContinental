from .auth import router as auth_router
from .users import router as users_router
from .reports import router as reports_router
from .recycling import router as recycling_router
from .schedules import router as schedules_router

__all__ = [
    'auth_router',
    'users_router',
    'reports_router',
    'recycling_router',
    'schedules_router'
]