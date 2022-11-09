from datetime import datetime, timedelta
from typing import List
from wsgiref.util import request_uri
from fastapi import APIRouter, Depends, Query
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from requests import request
from sqlalchemy import false
# from db.repository.search import search_job,  chu_30, movchoi, proc, order_register, order_recommend, order_s_count, order_read, search_celeb
# from db.repository.search import order_realtime, models_info, proc_celeb, img_mov_info, cf_mov_info, act_mov_info, best_img, get_rd_contracts
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.mypage import viewd_models, viewd_projects
from fastapi.encoders import jsonable_encoder
from striprtf.striprtf import rtf_to_text
from starlette.responses import RedirectResponse

import json, re
import pandas as pd

templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()


##### 모델료 코드 - >값
def code_to_mfee(models):
    
    with open("model.json", 'r', encoding='utf-8') as json_file:
        dict_model_fee = json.load(json_file)

    # print(models)
    for model in models:
        
        if not model['People']['isyeon'] and model['People']['mfee']:
            print(model)
            print(model['People']['mfee'])
            if dict_model_fee['model_fee'][model['People']['mfee']] == "4100~0":
                model['People']['mfee'] = "4100~"
            else:
                model['People']['mfee'] = dict_model_fee['model_fee'][model['People']['mfee']]
#######

@router.get("")
def my_page(request: Request, db: Session = Depends(get_db)):

     # 유저 token 유효성
    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/user')

    if token:
        
 
        return templates.TemplateResponse(
            "home/index.html", {"request": request,
                                    "host" : request.url.hostname
                                   }
        )


@router.get("/viewed-models")
def get_viewd_models(request: Request, db: Session = Depends(get_db)):
    

    # 유저 token 유효성
    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/user')

    user_id: str = request.cookies.get("usr")

    models = viewd_models(db, user_id)
    code_to_mfee(models)
    

    for m in models:
        if m['People']['isyeon']:
            print(m)

    if token:
        
        # 30일추천, 영상초이, 프로카운트 세가지로 나누어서 res 보냄.
        return templates.TemplateResponse(
            "home/list-viewed_models.html", {"request": request,
                                    "host" : request.url.hostname,
                                    "models" : models
                                   }
        )



@router.get("/viewd-projects")
def get_viewd_projects(request: Request, db: Session = Depends(get_db)):
    

    # 유저 token 유효성
    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/user')

    user_id: str = request.cookies.get("usr")

    projects = viewd_projects(db, user_id)
   
    print(projects)
    
    if token:
        
        # 30일추천, 영상초이, 프로카운트 세가지로 나누어서 res 보냄.
        return templates.TemplateResponse(
            "home/list-viewd_projects.html", {"request": request,
                                    "host" : request.url.hostname,
                                    "projects" : projects
                                   }
        )


