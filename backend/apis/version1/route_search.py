from cgi import test
from datetime import datetime, timedelta
import json
from statistics import mode
from fastapi import APIRouter, Depends
from fastapi import Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pandas import array
# from db.repository.search import search_job,  chu_30, movchoi, proc, order_register, order_recommend, order_s_count, order_read, search_celeb
# from db.repository.search import   order_realtime, models_info, proc_celeb, img_mov_info, cf_mov_info, act_mov_info, best_img, get_rd_contracts

from db.repository.search import search_recommendation_month
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.encoders import jsonable_encoder
from striprtf.striprtf import rtf_to_text
from starlette.responses import RedirectResponse


templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()


@router.get("")
def search_celeb(request: Request, gender: str = 'm%w', age: str = '0%100', mfee: str = '0%4100', alpha: str = '0100%auto', recommendation_section: str = 'img%fav%act%new',
           db: Session = Depends(get_db)):

    # 유저 token 유효성
    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/user')

    list_gender, list_age, list_mfee, list_recommendation_section = gender.strip().split('%'), age.split('%'), mfee.strip().split('%') + alpha.strip().split('%'), recommendation_section.strip().split('%')
    filter_models = search_recommendation_month(db=db, gender=list_gender, age=list_age, mfee=list_mfee, recommendation_section=list_recommendation_section)
    

    with open("model.json", 'r', encoding='utf-8') as json_file:
        dict_model_fee = json.load(json_file)
        
    for model in filter_models:
        if not model['mfee'] == '':
            if dict_model_fee['model_fee'][model['mfee']] == "4100~0":
                model['mfee'] = "4100~"
            else:
                model['mfee'] = dict_model_fee['model_fee'][model['mfee']]

    print('성별 :: ', gender.strip(), len(gender.strip()))
    print('나이 :: ', age.strip())
    print('모델료 :: ', mfee.strip())
    print('모델료 옵션 선택 :: ', alpha.strip())
    print('추천 점수 옵션 선택 :: ', recommendation_section.strip())

    # try:

   

    if token:
       
        # 30일추천, 영상초이, 프로카운트 세가지로 나누어서 res 보냄.
        return templates.TemplateResponse(
            "home/list-models.html", {"request": request,
                                        "preSelectValue": {"gender" : gender, "age" : age, "mfee": mfee, "alpha" : alpha, "recommendation_section" : recommendation_section},
                                        "test": filter_models}
        )

    # except:
    #     print('?')



