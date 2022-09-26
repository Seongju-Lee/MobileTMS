from fastapi import APIRouter
from apis.version1 import route_login
from apis.version1 import route_models
from apis.version1 import route_search
from apis.version1 import route_file

api_router = APIRouter()

api_router.include_router(route_login.router, prefix="/user", tags=["로그인"])
api_router.include_router(route_search.router, prefix="/search", tags=["모델검색 관련"])
api_router.include_router(route_models.router, prefix="/models", tags=["모델 탭"])
api_router.include_router(route_file.router, prefix="/files", tags=["모델 첨부파일"])
