from fastapi import APIRouter

from app.api.routes import login
from app.api.routes import users
from app.api.routes.items import items_controller
from app.api.routes.utils import utils_controller

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils_controller.router)
api_router.include_router(items_controller.router)

