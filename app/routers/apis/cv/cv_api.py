from fastapi import APIRouter, Request
from app.services.google import ServiceManager
from app.services.info_manager import InformationalServiceManager
from app.models.user import ClientHost
from loguru import logger

cv_router = APIRouter()


@cv_router.get("/proyects")
async def home(request: Request):
    logger.debug("getting all the proyects")
    key = request.session
    logger.debug(f"getting session id {key}")
    #proyects = InformationalServiceManager().get_proyects()
    proyects = {"test":"test"}
    return proyects