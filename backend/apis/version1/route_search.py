from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from fastapi import Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pandas import array
# from db.repository.search import search_job,  chu_30, movchoi, proc, order_register, order_recommend, order_s_count, order_read, search_celeb
# from db.repository.search import   order_realtime, models_info, proc_celeb, img_mov_info, cf_mov_info, act_mov_info, best_img, get_rd_contracts

from db.repository.search import search_test
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.encoders import jsonable_encoder
from striprtf.striprtf import rtf_to_text
from starlette.responses import RedirectResponse


templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()

test_models = []
@router.get("")
def models(request: Request, gender: str = 'm%w', age: str = '0%100', mfee: str = '0%4100', alpha: str = '0100%auto',
           db: Session = Depends(get_db)):

    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]

    list_gender, list_age, list_mfee = gender.split('%'), age.split('%'), mfee.split('%') + alpha.split('%')

    
    global test_models

    if test_models:
        print('존재')
        pass
    else:
        print('불러옴')
        test_models = search_test(db=db)
    
    print('성별 :: ', gender)
    print('나이 :: ', age)
    print('모델료 :: ', mfee)
    print('모델료 옵션 선택 :: ', alpha)

    try:

        token: str = request.cookies.get("access_token")
        user_id: str = request.cookies.get("usr")

        if token is None:
            return RedirectResponse('/user')

        else:

            # 30일추천, 영상초이, 프로카운트 세가지로 나누어서 res 보냄.
            return templates.TemplateResponse(
                "home/list-models.html", {"request": request,
                                          "preSelectValue": {"gender" : gender, "age" : age, "mfee": mfee, "alpha" : alpha},
                                          "test": test_models}
            )

    except:
        print('?')



