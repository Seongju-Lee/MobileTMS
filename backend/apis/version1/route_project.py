from datetime import datetime, timedelta
import json
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pandas import read_sql_table

from db.repository.project import get_project
from db.session import get_db
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder

templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()



# 프로젝트 검색
@router.get("")
def get_projects(request: Request, db: Session = Depends(get_db)):


    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/user')

    projects = get_project(db=db)


    projects = jsonable_encoder(projects[:])


    for project in projects:
        print(project)
        
    return templates.TemplateResponse(
            "home/list-projects.html", {"request": request, "projects": projects}
        )

  

    

