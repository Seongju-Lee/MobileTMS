from fastapi import APIRouter
from apis.version1 import route_login
from apis.version1 import route_models
from apis.version1 import route_search
from apis.version1 import route_file
from apis.version1 import route_celebs
from apis.version1 import route_project
from apis.version1 import route_me
from apis.version1 import route_log

api_router = APIRouter()

api_router.include_router(route_login.router, prefix="/user", tags=["로그인"])
api_router.include_router(route_search.router, prefix="/search", tags=["모델검색 리스트"])
api_router.include_router(route_models.router, prefix="/models", tags=["모델 탭"])
api_router.include_router(route_file.router, prefix="/files", tags=["모델 첨부파일"])
api_router.include_router(route_celebs.router, prefix="/celebs", tags=["셀럽검색 리스트"])
api_router.include_router(route_project.router, prefix="/projects", tags=["프로젝트 검색 리스트"])
api_router.include_router(route_me.router, prefix="/me", tags=["마이페이지 항목"])
api_router.include_router(route_log.router, tags=["로그 업데이트"])
