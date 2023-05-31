from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.google import ServiceManager
from app.services.info_manager import InformationalServiceManager
from app.models.user import ClientHost
from loguru import logger

cv_router = APIRouter()


@cv_router.get("/proyects")
async def home(request: Request):
    proyects = InformationalServiceManager().get_proyects()
    request.app.logger.debug("Debug test")
    return proyects