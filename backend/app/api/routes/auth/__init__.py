from fastapi import APIRouter

from app.api.routes.auth import auth_controller
from app.api.routes.auth import password_recovery_controller
from app.api.routes.auth import login_google_controller

router = APIRouter()
router.include_router(auth_controller.router)
router.include_router(password_recovery_controller.router)
router.include_router(login_google_controller.router)
