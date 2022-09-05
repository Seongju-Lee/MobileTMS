from fastapi import APIRouter
from apis.version1 import route_login
from apis.version1 import route_models

api_router = APIRouter()

api_router.include_router(route_login.router, prefix="/user", tags=["로그인"])
api_router.include_router(route_models.router, prefix="/models", tags=["모델검색 관련"])
