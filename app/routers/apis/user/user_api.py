from fastapi import APIRouter,Request
from fastapi.responses import RedirectResponse
from app.services.google import ServiceManager
from app.models.session import Token

user_router = APIRouter()

@user_router.post("/userdata")
async def user_info(request: Request):
    #background_tasks.add_task(message="some notification")
    ServiceManager().get_service()
    return 'funciona'

@user_router.get("/generate-session")
async def create_access(request:Request):

    serviceManager = ServiceManager()
    isValidSession = serviceManager.validate_credentials()
    if isValidSession:
        return serviceManager.get_credentials()
    

@user_router.get("/generate-url")
async def create_access():
    return RedirectResponse(ServiceManager().generate_url())

@user_router.get("/clearaccess")
async def create_access():
    return ServiceManager().clear_access()