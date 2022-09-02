from fastapi import APIRouter
from apis.version1 import route_login

api_router = APIRouter()

api_router.include_router(route_login.router, prefix="/user", tags=["login"])
