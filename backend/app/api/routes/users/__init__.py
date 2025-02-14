from fastapi import APIRouter

from app.core.config import settings
from app.api.routes.users import (
  private_controller,
  users_controller,
  admin_users_controller,
  self_user_controller,
)

router = APIRouter()
router.include_router(self_user_controller.router)
# users_controller andd admin_users_controller should always be the last one because it has dynamic path
router.include_router(admin_users_controller.router)
router.include_router(users_controller.router)

if settings.ENVIRONMENT == "local":
    router.include_router(private_controller.router)