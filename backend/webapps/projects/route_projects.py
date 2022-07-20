from audioop import reverse
from datetime import datetime, timedelta
from turtle import rt
from fastapi import APIRouter, Depends
from fastapi import Request, status, responses, Response, requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.encoders import jsonable_encoder
from striprtf.striprtf import rtf_to_text
from starlette.responses import RedirectResponse
from db.repository.project import get_project, get_filter_project, get_project_info, get_project_memo, get_project_model, get_project_with, project_security
from webapps.auth.forms import LoginForm

import json
import pandas as pd


templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()


@router.get("/p/{pcode}")
def project(request: Request, db: Session = Depends(get_db), pcode:str=''):
    
    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/login')


    info = get_project_info(db=db, pcode=pcode)
    info = jsonable_encoder(info[:])
    
    pmemo = get_project_memo(db, pcode)
    pmemo = jsonable_encoder(pmemo[:])

    models = get_project_model(db, pcode)
    models = jsonable_encoder(models[:])

    for model in models:
        model['chunggu'] = format(model['chunggu'], ',')    
        model['modelfee'] = format(model['modelfee'], ',')    
            
    
        
    ## 보안 프로젝트
    if info[0]['boan19ca'] or info[0]['boan19']:

        user: str = request.cookies.get("usr")

        team_scrty = info[0]['boan19ca'].split('/')
        admin_scrty = info[0]['boan19'].split('/')
        
        team_scrty.remove('')
        admin_scrty.remove('')

        scrty = project_security(db, user, pcode, team_scrty, admin_scrty)


        if not scrty:

            return templates.TemplateResponse(
                    "project_info.html", {"request": request, "info": '보안'}
            )


    try:
        memo = rtf_to_text(pmemo[0]['memo']) # memo 없으면 except
        memos = memo.split('\n\n')


        memo_ = []
        for i in memos:
            memo_.append(i.split('\n'))
        
        return templates.TemplateResponse(
                "project_info.html", {"request": request, "info": info[0], "memos": memo_, "models": models}
        )


    except:

        return templates.TemplateResponse(
                "project_info.html", {"request": request, "info": info[0], "models": models}
        )


    

@router.get("/p")
def home(request: Request, db: Session = Depends(get_db),
project_name: str = '',
rd_team: str = '',
cf_owner: str = '',
cf_regdate: str = '',
entertainment: str = '',
isceleb: str=''):

    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]
 
    # try:
        
    token: str = request.cookies.get("access_token")

    if token is None:
        return RedirectResponse('/login')
    

    # 아무것도 입력안하고, 처음 경로로 들어오면 모든 프로젝트 검색
    elif not project_name and not rd_team and not cf_owner and not cf_regdate:

        a_project = get_project(db=db)
        a_project = list(jsonable_encoder(a_project[:]))
        
        return templates.TemplateResponse(
            "project-table.html", {"request": request,
                        "years": years,  "now_year": now_year, "a_project": a_project}
        )



    if entertainment:
        ## 레디 진행이력 프로젝트 검색

        search_project = get_project_with(db, entertainment)
        search_project = sorted(search_project , key= lambda x: x['cdate'], reverse=True)

        return templates.TemplateResponse(
                "entertainment_project.html", {"request": request,
                            "years": years,  "now_year": now_year, 'entertainment_project': search_project, 'entertainment': entertainment}
        )


    else:
        # 검색 필터에 맞는 프로젝트만 검색
        filter_project = get_filter_project(db=db, project_name=project_name, rd_team=rd_team, cf_owner=cf_owner, cf_regdate=cf_regdate, isceleb=isceleb)

        f_project = (jsonable_encoder(filter_project[:]))
        f_project = list(reversed(f_project))


        return templates.TemplateResponse(
                "project-table.html", {"request": request,
                            "years": years,  "now_year": now_year, "a_project": f_project}
        )
        
    
    # except:
    #     print('?')
