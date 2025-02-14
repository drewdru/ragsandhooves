from fastapi import APIRouter

from app.api.routes.login import login_controller
from app.api.routes.login import password_recovery_controller

router = APIRouter()
router.include_router(login_controller.router)
router.include_router(password_recovery_controller.router)
