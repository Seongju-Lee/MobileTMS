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

api_router.include_router(route_login.router, prefix="/login", tags=["login"])
