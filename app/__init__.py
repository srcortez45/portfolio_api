from contextlib import asynccontextmanager
from app.routers import router_api
from app.models.loglevel import LogLevel
from app.utils.settings import cnf
from app.utils.config import NotificationManager, NotificationState
from loguru import logger
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
import time
import sys

@asynccontextmanager
async def lifespan(app: FastAPI):
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
        lifespan=lifespan)
    app.include_router(prefix='/v1',
                       router=router_api)
    notifier = NotificationManager(app)
    app.state._state["notifier_manager"] = notifier
    app.state._state["notifier_state"] = NotificationState(notifier)
    return app


app = get_application()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def read_root():
  logger.debug("accesing docs")
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

@app.put("/api/log/{level}")
async def change_log_level(level,request:Request):
    logging_level = LogLevel.set_log_level(level)
    logger.remove()
    logger.add(sys.stderr, level=logging_level)
    request.app.state.mode = logging_level
    notifier:NotificationManager = request.app.state._state.get("notifier_manager")
    notifier.log_level = logging_level
    return {"level":logging_level}


app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SessionMiddleware, secret_key="secret_key")