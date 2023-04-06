from fastapi import APIRouter,Request
from fastapi.responses import RedirectResponse
from app.services.google import ServiceManager
from app.supabase.client import ClientManager
import uuid

user_router = APIRouter()

@user_router.get("/cred")
async def get_cred(request: Request):
    


    ClientManager().save_session()

    return None

    #response = supabase.table('info').select("*").execute()
    #print(response)
    #ServiceManager().get_client_credentials()  

@user_router.post("/userdata")
async def user_info():
    #background_tasks.add_task(message="some notification")
    ServiceManager().get_service()
    return 'funciona'

@user_router.get("/generate-session")
async def create_access(request:Request):
    print(request.session.get("uuid4", None))
    return 'test'
    #return ServiceManager().create_session(request.url._url)

@user_router.get("/generate-url")
async def generate_url_access(request:Request):
    request.session["uuid4"] = str(uuid.uuid4())
    print(request.state.db)
    print(request.session.get("uuid4", None))
    #return request.cookies.get('session')
    return RedirectResponse(ServiceManager().generate_url())

@user_router.get("/clearaccess")
async def clear_access():
    return ServiceManager().clear_access()