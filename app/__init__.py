from contextlib import asynccontextmanager
from app.routers import router_api
from app.utils.settings import cnf
from loguru import logger
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
import time
import sys

@asynccontextmanager
async def lifespan(app: FastAPI):
    #logger.remove()
    #logger.add(sys.stderr, level="INFO")
    logger.debug("DEBUG MODE")
    logger.info("STARTING APP")
    yield
    logger.debug("SHUTDOWN APP")


def get_application():

    app = FastAPI(
        title = cnf.TITLE,
        description = cnf.APP_CONFIG.DESCRIPTION,
        version = cnf.APP_CONFIG.VERSION,
        openapi_tags=cnf.APP_CONFIG.tags_metadata,
        openapi_url = cnf.openapi_url,
        docs_url=cnf.docs_url,
        lifespan=lifespan
        )
    app.include_router(prefix='/v1',
                       router=router_api)
    return app

app = get_application()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response



app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)

@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    session = request.cookies.get('session')
    if session:
        response.set_cookie(key='session',
                            value=request.cookies.get('session'),
                            httponly=True)
    return response

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/")
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }