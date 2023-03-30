from app.routers.apis.user.user_api import user_router
from app.utils.settings import cnf

from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
import time

def get_application():

    app = FastAPI(
        title = cnf.TITLE,
        description = cnf.APP_CONFIG.DESCRIPTION,
        version = cnf.APP_CONFIG.VERSION,
        openapi_tags=cnf.APP_CONFIG.tags_metadata,
        openapi_url = cnf.openapi_url,
        docs_url=cnf.docs_url,
        redoc_url= cnf.redoc_url
        )
    app.include_router(user_router)
    return app

app = get_application()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/", tags=["Root"])
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }