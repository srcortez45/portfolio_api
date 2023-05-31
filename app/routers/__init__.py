from fastapi import APIRouter
from app.routers.apis.user.user_api import user_router
from app.routers.apis.cv.cv_api import cv_router
from app.utils.settings import cnf

router_api = APIRouter()
router_api.include_router(prefix='/user',
                          router=user_router,
                          tags=['google auth'])
router_api.include_router(prefix='/cv',
                          router=cv_router,
                          tags=['user cv'])