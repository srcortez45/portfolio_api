from contextlib import asynccontextmanager
from app.routers.apis.user.user_api import user_router
from app.utils.settings import cnf
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('starting db session')
    redis = aioredis.from_url( url=cnf.REDIS,
                               encoding="utf8", 
                               decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()
    print('shutdown db session')


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
    app.include_router(router=user_router,
                       prefix='/session')
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


@app.get("/", tags=["Root"])
@cache(expire=180)
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }