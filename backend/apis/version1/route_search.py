from datetime import datetime, timedelta
import json
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pandas import read_sql_table

from db.repository.search import search_recommendation_month, search_mov_choi, search_procount, search_real_time, search_open_count, search_scount, search_recommend
from db.session import get_db
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse


templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()


def code_to_mfee(models):


    with open("model.json", 'r', encoding='utf-8') as json_file:
        dict_model_fee = json.load(json_file)

    for model in models:
        if not model['mfee'] == '':
            if dict_model_fee['model_fee'][model['mfee']] == "4100~0":
                model['mfee'] = "4100~"
            else:
                model['mfee'] = dict_model_fee['model_fee'][model['mfee']]


@router.get("")
def get_search(request: Request, category: str, gender: str = 'm%w', age: str = '1%100', mfee: str = '150%4100', cfee: str = '0%10',alpha: str = '0100%auto', recommendation_section: str = 'img%fav%act%new', section: str = "singer%actor%idol%entertainment%broadcast%celeb%youtube%", period: str = "a_3",
           db: Session = Depends(get_db)):


    token: str = request.cookies.get("access_token")
    if token is None:
        return RedirectResponse('/user')

    # K모델
    if category == 'kmodels' and token:
        
        return templates.TemplateResponse(
            "home/list-models.html", get_search_models(request, gender, age, mfee, alpha, recommendation_section, db)
        )

    if category == 'celeb' and token:
        
        return templates.TemplateResponse(
            "home/list-celeb.html", get_search_celebs(request, gender, age, cfee, section,period ,db)
        )

    if category == 'sunok' and token:
        
        return templates.TemplateResponse(
            "home/list-sunokstar.html", get_search_sunok(request, gender, age, cfee, section,period ,db)
        )



def get_search_models(request: Request, gender: str = 'm%w', age: str = '1%100', mfee: str = '150%4100', alpha: str = '0100%auto', recommendation_section: str = 'img%fav%act%new',
           db: Session = Depends(get_db)):

    

    list_gender, list_age, list_mfee, list_recommendation_section = gender.strip().split('%'), age.split('%'), mfee.strip().split('%') + alpha.strip().split('%'), recommendation_section.strip().split('%')
    

    month_models = search_recommendation_month(db=db, gender=list_gender, age=list_age, mfee=list_mfee, recommendation_section=list_recommendation_section)
    mov_choi_models = search_mov_choi(db=db, gender=list_gender, age=list_age, mfee=list_mfee)
    procount_models =  search_procount(db=db, gender=list_gender, age=list_age, mfee=list_mfee)

    
    code_to_mfee(month_models)
    code_to_mfee(mov_choi_models)    
    code_to_mfee(procount_models)


    
    return {"request": request,
            "preSelectValue": {"gender" : gender, "age" : age, "mfee": mfee, "alpha" : alpha, "recommendation_section" : recommendation_section},
            "recommendation_month": month_models,
            "mov_choi": mov_choi_models,
            "procount": procount_models}



def get_search_celebs(request: Request, gender: str = 'm%w', age: str = '1%100', cfee: str = '0%00', section: str = "singer%actor%idol%entertainment%broadcast%celeb%youtube%", period: str = 'a_3',
           db: Session = Depends(get_db)):

    
  
    list_gender, list_age, list_cfee, list_section = gender.strip().split('%'), age.split('%'), cfee.strip().split('%'), section.strip().split('%')

    try:
        list_section.remove('')
    except:
        pass

    # 실베스타
    real_time_models = search_real_time(db, list_gender,list_age, list_cfee,  list_section, period)

    # 열람횟수
    read_count_models = search_open_count(db, list_gender,list_age, list_cfee,  list_section, period)

    return {"request": request,
            "preSelectValue": {"gender" : gender, "age" : age, "cfee": cfee, "section" : section, "period" : period},
            "real_time_models": real_time_models,
            "read_count_models": read_count_models}





def get_search_sunok(request: Request, gender: str = 'm%w', age: str = '1%100', cfee: str = '0%00', section: str = "singer%actor%idol%entertainment%broadcast%celeb%youtube%", period: str = 'a_3',
           db: Session = Depends(get_db)):

    
  
    list_gender, list_age, list_cfee, list_section = gender.strip().split('%'), age.split('%'), cfee.strip().split('%'), section.strip().split('%')

    try:
        list_section.remove('')
    except:
        pass
    

    print('sunokStar 분류 값 :: ', list_gender, list_age, list_cfee, list_section)
    
    # S카운트순
    scount_models = search_scount(db, list_gender,list_age, list_cfee,  list_section, period)



    # 열람횟수
    recommend_models = search_recommend(db, list_gender,list_age, list_cfee,  list_section, period)

    return {"request": request,
            "preSelectValue": {"gender" : gender, "age" : age, "cfee": cfee, "section" : section, "period" : period},
            "scount_models" : scount_models,
            "recommend_models" : recommend_models
            }

