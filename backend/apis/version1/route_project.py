from datetime import datetime, timedelta
import json
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pandas import read_sql_table

from db.repository.project import get_project, get_filter_project, get_project_information, get_project_file
from db.session import get_db
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()



# 프로젝트 검색
@router.get("")
def get_projects(request: Request, team: str = '', prname: str = '', cfowner: str='', cfco: str='', pryear: str='2000%2022', entertainment: str='', db: Session = Depends(get_db)):


    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/user')

    # projects = get_project(db=db)
    # projects = jsonable_encoder(projects[:])


    pryear = [x+int(pryear.split('%')[0]) for x in range(0, (int(pryear.split('%')[1]) - int(pryear.split('%')[0]) )+1 ) ]

    print(pryear)
    projects = get_filter_project(db, team, prname, cfowner, cfco, pryear)
    projects = jsonable_encoder(projects[:])

    # print("TQ 좀")
    # print(jsonable_encoder(kk[:]))

    teamtag = ['All' , 'C1-1', 'C1-2', 'C2-1', 'C2-2', 'C3-1','C3-2', 'C3-3', 'C4-1', 'C4-2', 'C5-1', 'C5-2', 'C6-1', 'C6-2',
                'G1', 'IP', 'INFL', 'PPL', 'DRAMA', '뮤즈A', '뮤즈B', '레디차이나', '',
                '명유미', '이순옥', '조선아', '문인옥', '김다애', '서동혁', '',
                '구기운', '최영상', 'KOO최']
        
    return templates.TemplateResponse(
            "home/list-projects.html", {"request": request, "projects": projects, "team_list" : teamtag}
        )

  

# 프로젝트 검색
@router.get("/{pcode}")
def get_project_info(request: Request, pcode: str, db: Session = Depends(get_db)):

    # 연락처 등, 프로젝트 기본 정보
    project_info = get_project_information(db, pcode)
    #프로젝트 첨부파일
    project_files = get_project_file(db, pcode)

    project_info = jsonable_encoder(project_info[:])
    project_files = jsonable_encoder(project_files[:])



    # print('프로젝트 상세 정보입니다 ::', project_info)
    print('프로젝트 첨부파일 입니다. ::', project_files[:])
    
    
    return templates.TemplateResponse(
            "home/info-project.html", {"request": request, "project_info": project_info[0], "project_files": project_files}
        )


