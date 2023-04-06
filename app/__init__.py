from contextlib import asynccontextmanager
from app.routers.apis.user.user_api import user_router
from app.utils.settings import cnf

from app.supabase.client import ClientManager

from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request, Depends, Response
import time



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    print('starting db session')

    db_local = ClientManager().get_client()

    #ClientManager().get_client().auth.set_session()

    yield

    print(db_local.auth.get_session())
    #print(credentials)
    
    #self.get_client().auth.set_session()

    #self.get_client().auth._remove_session()

    print('shutdown db session')

def get_db():
    db = 'session open'
    try:
        yield db
    finally:
        print('closing connection')


def get_application():

    app = FastAPI(
        title = cnf.TITLE,
        description = cnf.APP_CONFIG.DESCRIPTION,
        version = cnf.APP_CONFIG.VERSION,
        openapi_tags=cnf.APP_CONFIG.tags_metadata,
        openapi_url = cnf.openapi_url,
        docs_url=cnf.docs_url,
        lifespan=lifespan,
        dependencies=[Depends(get_db)]
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

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = 'value'
        response = await call_next(request)
    finally:
        request.state.db = None
    return response


app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/", tags=["Root"])
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }