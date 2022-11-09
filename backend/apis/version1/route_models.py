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
from db.repository.model import model_info, model_point_memo, mov_list, get_model_cf, get_tel_memo
from db.repository.project import get_kmodel_project
from fastapi.encoders import jsonable_encoder
from striprtf.striprtf import rtf_to_text
from starlette.responses import RedirectResponse

import json, re
import pandas as pd

templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()


##### 모델료 코드 - >값
def code_to_mfee(model):
    

    
    with open("model.json", 'r', encoding='utf-8') as json_file:
        dict_model_fee = json.load(json_file)

    print(model)
    if not model['mfee'] == '':
        if dict_model_fee['model_fee'][model['mfee']] == "4100~0":
            model['mfee'] = "4100~"
        else:
            model['mfee'] = dict_model_fee['model_fee'][model['mfee']]
#######



@router.get("/{codesys}/{mov_section}")
def get_mov_file(req: Request, codesys: str = '', mov_section: str = '',db: Session = Depends(get_db)):


    res_mov = mov_list(db=db, codesys=codesys, mov_section=mov_section)
    res_mov = jsonable_encoder(res_mov[:])

    print('ghhhh', req.url.hostname)

    
    for mov in res_mov:
        print(mov)

    if not res_mov:
        
        return templates.TemplateResponse(
                "home/attachments-list.html", {"request": req, "text": '존재하지 않습니다.'}
    )
    else:
        return templates.TemplateResponse(
                "home/attachments-list.html", {"request": req, "attachments": res_mov}
    )



@router.get("/{codesys}")
def get_model_info(request: Request, codesys: str = '', db: Session = Depends(get_db)):
    

    # 유저 token 유효성
    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/user')

    print('OK codesys :: ', codesys)


    model = model_info(db, codesys)[0]
    point_memo_list = model_point_memo(db, codesys)
    project_list = get_kmodel_project(db, codesys)
    cf_list, cf_list_end = get_model_cf(db, codesys)
    tel_memo_list = get_tel_memo(db, codesys)
    tel_memo_list = jsonable_encoder(tel_memo_list[:])

    code_to_mfee(model)




    for constract in project_list[:]:
        constract['modelfee'] = format(constract['modelfee'], ',')

    model['project_list'] = project_list
    model['cf_list'] = cf_list
    model['cf_list_end'] = cf_list_end
    model['tel_memo'] = tel_memo_list
    model['point2'] = rtf_to_text(point_memo_list[0]['point2'])
    model['point2'] = model['point2'].split('\n')

    # print(model)


   
    is_existed_img = 'primary' if jsonable_encoder(mov_list(db=db, codesys=codesys, mov_section='img')[:]) else 'danger'

    is_existed_act = 'primary' if jsonable_encoder(mov_list(db=db, codesys=codesys, mov_section='act')[:]) else 'danger'

    is_existed_cf = 'primary' if jsonable_encoder(mov_list(db=db, codesys=codesys, mov_section='cf')[:]) else 'danger'

    is_existed_best = 'primary' if jsonable_encoder(mov_list(db=db, codesys=codesys, mov_section='b')[:]) else 'danger'

    is_existed_refer = 'primary' if jsonable_encoder(mov_list(db=db, codesys=codesys, mov_section='r')[:]) else 'danger'

    if token:
           
        # 30일추천, 영상초이, 프로카운트 세가지로 나누어서 res 보냄.
        return templates.TemplateResponse(
            "home/info-model.html", {"request": request,
                                    "model_detail_info": model,
                                    "host" : request.url.hostname,
                                    "is_existed_img": is_existed_img,
                                    "is_existed_act": is_existed_act,
                                    "is_existed_cf": is_existed_cf,
                                    "is_existed_best" : is_existed_best,
                                    "is_existed_refer" : is_existed_refer}
        )


