from datetime import datetime, timedelta
import json
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates

from db.repository.search import search_recommendation_month, search_mov_choi, search_procount
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
def get_search(request: Request, category: str, gender: str = 'm%w', age: str = '1%100', mfee: str = '150%4100', cfee: str = '0%10',alpha: str = '0100%auto', recommendation_section: str = 'img%fav%act%new',
           db: Session = Depends(get_db)):

    print('category 확인 :: ', category)

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
            "home/list-celeb.html", get_search_celebs(request, gender, age, cfee, db)
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

    
    return {"request": request, "preSelectValue": {"gender" : gender, "age" : age, "mfee": mfee, "alpha" : alpha, "recommendation_section" : recommendation_section},
                                        "recommendation_month": month_models,
                                        "mov_choi": mov_choi_models,
                                        "procount": procount_models}



def get_search_celebs(request: Request, gender: str = 'm%w', age: str = '1%100', cfee: str = '0%00',
           db: Session = Depends(get_db)):

    

    list_gender, list_age, list_cfee = gender.strip().split('%'), age.split('%'), cfee.strip().split('%')
    

    # month_models = search_recommendation_month(db=db, gender=list_gender, age=list_age, mfee=list_cfee)
    # mov_choi_models = search_mov_choi(db=db, gender=list_gender, age=list_age, mfee=list_cfee)
    # procount_models =  search_procount(db=db, gender=list_gender, age=list_age, mfee=list_cfee)

    # # code_to_mfee(month_models)
    # code_to_mfee(mov_choi_models)    
    # code_to_mfee(procount_models)

    
    return {"request": request, "preSelectValue": {"gender" : gender, "age" : age, "cfee": cfee},
                                       }



