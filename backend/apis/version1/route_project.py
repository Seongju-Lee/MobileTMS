from cmath import pi
from datetime import datetime, timedelta
import json
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pandas import read_sql_table

from db.repository.project import get_project, get_filter_project, get_project_information, get_project_file, get_project_contract, get_project_memo, get_project_with, project_security

from db.session import get_db
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from striprtf.striprtf import rtf_to_text

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

    
    projects = get_filter_project(db, team, prname, cfowner, cfco, pryear)
    projects = jsonable_encoder(projects[:])



    teamtag = ['All' , 'C1-1', 'C1-2', 'C2-1', 'C2-2', 'C3-1','C3-2', 'C3-3', 'C4-1', 'C4-2', 'C5-1', 'C5-2', 'C6-1', 'C6-2',
                'G1', 'IP', 'INFL', 'PPL', 'DRAMA', '뮤즈A', '뮤즈B', '레디차이나', '',
                '명유미', '이순옥', '조선아', '문인옥', '김다애', '서동혁', '',
                '구기운', '최영상', 'KOO최']
        

    if entertainment:
        projects_with = get_project_with(db, entertainment)
        projects_with = jsonable_encoder(projects_with[:])
        projects_with = sorted(projects_with , key= lambda x: x['cdate'], reverse=True)
        
        print(projects_with[0])
        return templates.TemplateResponse(
            "home/list-projects_with.html", {"request": request, "projects": projects_with, "team_list" : teamtag}
        )
    


    
    return templates.TemplateResponse(
            "home/list-projects.html", {"request": request, "projects": projects, "team_list" : teamtag}
        )

  

# 프로젝트 검색
@router.get("/{pcode}")
def get_project_info(request: Request, pcode: str, db: Session = Depends(get_db)):


    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/user')
        
    # 연락처 등, 프로젝트 기본 정보
    project_info = get_project_information(db, pcode)
    #프로젝트 첨부파일
    project_files, estimate_file = get_project_file(db, pcode)
    # 프로젝트 관련모델
    contract_models = get_project_contract(db, pcode)
    # 프로젝트 통화메모
    project_memo = get_project_memo(db, pcode)



    project_info = jsonable_encoder(project_info[:])
    project_files = jsonable_encoder(project_files[:])
    estimate_files = jsonable_encoder(estimate_file[:])
    contract_models = jsonable_encoder(contract_models[:])
    project_memo = jsonable_encoder(project_memo[:])



    print(project_info)


    


    try:
    
        project_memo[0]['memo'] = rtf_to_text(project_memo[0]['memo'])
        
    except:
        pass

    for model in contract_models[:]:
        model['chunggu'] = format(model['chunggu'], ',')
        model['modelfee'] = format(model['modelfee'], ',')
    


    if project_info[0]['boan19ca'] or project_info[0]['boan19']:
        
        user: str = request.cookies.get("usr")

        team_scrty = project_info[0]['boan19ca'].split('/')
        admin_scrty = project_info[0]['boan19'].split('/')
        
        team_scrty.remove('')
        admin_scrty.remove('')


        print(team_scrty, admin_scrty)
        is_scrty = project_security(db, user, pcode, team_scrty, admin_scrty)
        print(is_scrty)

        return templates.TemplateResponse(
            "home/info-project.html", {"request": request,
                                        "host" : request.url.hostname + ":8000",
                                        "project_info": project_info[0],
                                        "project_files": project_files,
                                        "estimate_files": estimate_files,
                                        "contract_models": contract_models,
                                        "project_memo": project_memo,
                                        "is_scrty": is_scrty}
        )
        
    return templates.TemplateResponse(
            "home/info-project.html", {"request": request,
                                        "host" : request.url.hostname + ":8000",
                                        "project_info": project_info[0],
                                        "project_files": project_files,
                                        "estimate_files": estimate_files,
                                        "contract_models": contract_models,
                                        "project_memo": project_memo,
                                        "is_scrty": False}
        )


