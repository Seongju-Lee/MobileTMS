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
from db.repository.project import get_project, get_filter_project, get_project_info, get_project_memo, get_project_model, get_project_with


import json
import pandas as pd


templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()


@router.get("/p/{pcode}")
def project(request: Request, db: Session = Depends(get_db), pcode:str=''):
    
    print('프로젝트 코드 출력 :: ', pcode)
    info = get_project_info(db=db, pcode=pcode)

    info = jsonable_encoder(info[:])
    print('해당 프로젝트 정보 :: ', info)
    

    try:
        pmemo = get_project_memo(db, pcode)
        pmemo = jsonable_encoder(pmemo[:])
        memo = rtf_to_text(pmemo[0]['memo'])
        memos = memo.split('\n\n')


        memo_ = []
        for i in memos:
            memo_.append(i.split('\n'))
        

        models = get_project_model(db, pcode)
        models = jsonable_encoder(models[:])

        for model in models:
            model['chunggu'] = format(model['chunggu'], ',')    
            model['modelfee'] = format(model['modelfee'], ',')    
                  
        print('project models :: ', models)

        token: str = request.cookies.get("access_token")



        if token is None:
            return RedirectResponse('/login')
        else:   
            return templates.TemplateResponse(
                    "project_info.html", {"request": request, "info": info[0], "memos": memo_, "models": models}
            )


    except:

        token: str = request.cookies.get("access_token")


        models = get_project_model(db, pcode)
        models = jsonable_encoder(models[:])

        print('project models :: ', models)


        if token is None:
            return RedirectResponse('/login')
        else:   
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
        a_project = (jsonable_encoder(a_project[:]))

        a_project = list(reversed(a_project))

        
        return templates.TemplateResponse(
            "project-table.html", {"request": request,
                        "years": years,  "now_year": now_year, "a_project": a_project}
        )



    if entertainment:
        ## 레디 진행이력 프로젝트 검색

        search_project = get_project_with(db, entertainment)
        print( 'project tabel create :: ' , len(search_project))
        

        return templates.TemplateResponse(
                "entertainment_project.html", {"request": request,
                            "years": years,  "now_year": now_year, 'entertainment_project': search_project, 'entertainment': entertainment}
        )


    else:
        # 검색 필터에 맞는 프로젝트만 검색
        print(project_name, rd_team, cf_owner, cf_regdate, isceleb)
        filter_project = get_filter_project(db=db, project_name=project_name, rd_team=rd_team, cf_owner=cf_owner, cf_regdate=cf_regdate, isceleb=isceleb)

        f_project = (jsonable_encoder(filter_project[:]))

        f_project = list(reversed(f_project))



        return templates.TemplateResponse(
                "project-table.html", {"request": request,
                            "years": years,  "now_year": now_year, "a_project": f_project}
        )
        
    
    # except:
    #     print('?')
