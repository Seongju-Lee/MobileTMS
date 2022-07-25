from fastapi import APIRouter
from webapps.models import route_models
from webapps.auth import route_login, route_log
from webapps.projects import route_projects

api_router = APIRouter(include_in_schema=False)

api_router.include_router(route_models.router, tags=["homepage"])
api_router.include_router(route_login.router, tags=["Auth"])
api_router.include_router(route_log.router, tags=["Log"])
api_router.include_router(route_projects.router, tags=["Project"])
