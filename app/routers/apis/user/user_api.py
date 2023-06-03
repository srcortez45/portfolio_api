from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.google import ServiceManager
from app.models.user import ClientHost
from loguru import logger
import uuid

user_router = APIRouter()


@user_router.get("/generate-url")
async def generate_url_access(request:Request):
    logger.debug("Generating url access")
    request.session["uuid4"] = request.session.get("uuid4", str(uuid.uuid4()))
    #client_ip = request.headers.get("ip-address", None)
    client_ip = request.client.host
    client = ClientHost(id = request.session.get("uuid4"),
                        ip = client_ip,
                        base_url = str(request.base_url))
    response = ServiceManager().generate_url(client)
    logger.debug("ServiceManager.generated_url")
    return JSONResponse(response)


@user_router.get("/generate-session")
async def create_access(request:Request):
    id = request.session.get("uuid4", None)
    return ServiceManager().session_flow(id, request.url._url)


@user_router.get("/refresh-session")
async def refresh_session(request:Request):
    id = request.session.get("uuid4", None)
    return ServiceManager().session_flow(id, request.url._url)


@user_router.get("/delete-session")
async def delete_access(request:Request):
    id = request.session.get("uuid4", None)
    return ServiceManager().delete_last_session(id)