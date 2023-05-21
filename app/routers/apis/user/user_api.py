from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.google import ServiceManager
from app.models.user import ClientHost
import uuid

user_router = APIRouter()


@user_router.get("/generate-url")
async def generate_url_access(request:Request):
    request.session["uuid4"] = request.session.get("uuid4", str(uuid.uuid4()))
    #client_ip = request.headers.get("ip-address", None)
    client_ip = request.client.host
    client = ClientHost(id = request.session.get("uuid4"),
                        ip = client_ip,
                        base_url = str(request.base_url))
    response = ServiceManager().generate_url(client)
    return JSONResponse(response)


@user_router.get("/generate-session")
async def create_access(request:Request):
    id = request.session.get("uuid4", None)
    return ServiceManager().session_flow(id, request.url._url)