from datetime import datetime
from pyexpat import model
from re import A
from statistics import mode
from time import time
import turtle
from fastapi import APIRouter, Depends
from fastapi import Request, status, responses, Response, requests
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.repository.jobs import list_jobs, search_job, list_models, chu_30, movchoi, proc, order_register, order_recommend
from db.repository.jobs import retrieve_job, create_new_job
from sqlalchemy import String,  null
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.users import User
from apis.version1.route_login import get_current_user_from_token
from webapps.jobs.forms import JobCreateForm
from schemas.jobs import JobCreate
from typing import Optional
from fastapi.encoders import jsonable_encoder
import pandas as pd

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):

    now_year = datetime.today().year
    years = [i for i in range(now_year-10, 1930, -1)]

    return templates.TemplateResponse(
        "index.html", {"request": request,
                       "years": years,  "now_year": now_year}
    )


@router.get("/detail/{id}")
def job_detail(id: int, request: Request, db: Session = Depends(get_db)):
    job = retrieve_job(id=id, db=db)
    return templates.TemplateResponse(
        "jobs/detail.html", {"request": request, "job": job}
    )


######################
# 날짜, 성별, 연령 등 필터들 예외처리 해놔야 함.
# 필터내용
@ router.get("/filter")
def search_filter(req: Request, s_date: str = '', e_date: str = '', gender_m: str = '', gender_w: str = '',
                  s_img: str = '', e_img: str = '', s_fav: str = '', e_fav: str = '', s_act: str = '', e_act: str = '', s_age: str = '', e_age: str = '', model: str = '', celeb: str = '',
                  sort_thrdays: str = '', sort_movchoi: str = '', sort_proc: str = '', sort_register: str = '', sort_recommend: str = '', sort_s_count: str = '',
                  db: Session = Depends(get_db)):

    now_year = datetime.today().year
    years = [i for i in range(now_year-10, 1930, -1)]
    if not (sort_thrdays or sort_movchoi or sort_proc or sort_register or sort_recommend):
        return templates.TemplateResponse(
            "ui-icons.html", {"request": req}
        )

    print('나이 구간 입력: ', s_age, e_age)
    print(model, celeb)

    ###########################################
    # 추천 30일
    if sort_thrdays:
        models = chu_30(db=db, chu_act=s_act,
                        chu_fav=s_fav, chu_img=s_img, gender_m=gender_m, gender_w=gender_w, s_age=s_age, e_age=e_age)

        img_ok, fav_ok, act_ok = False, False, False
        chu_models = jsonable_encoder(models[:])
        res_models = []
        i = 0
        print(chu_models)
        df = pd.DataFrame(chu_models).groupby(
            ['mcode', 'gubun', 'name']).sum().reset_index()

        search_models = df.values.tolist()
        # print(search_models)
        filter_models = []
        output_models = []
        for model in (search_models):
            # print(': ', model)
            if model[1] == 'act':
                res_models.append(
                    {'mcode': model[0], 'gubun': model[1], 'name': model[2], 'act_jum': model[3]})
            elif model[1] == 'fav':
                res_models.append(
                    {'mcode': model[0], 'gubun': model[1], 'name': model[2], 'fav_jum': model[3]})
            elif model[1] == 'img':
                res_models.append(
                    {'mcode': model[0], 'gubun': model[1], 'name': model[2], 'img_jum': model[3]})

            if len(res_models) != i:
                # print(': ', res_models[i])
                # print('::: ', res_models[i])
                if res_models[i]['mcode'] == res_models[i-1]['mcode']:

                    res_models[i].update(res_models[i-1])
                else:
                    filter_models.append(res_models[i-1])

                i += 1

        filter_models.append(res_models[i-1])  # 마지막 모델 추가
        for model in filter_models:

            if not 'img_jum' in model.keys():
                model['img_jum'] = 0
            if not 'fav_jum' in model.keys():
                model['fav_jum'] = 0
            if not 'act_jum' in model.keys():
                model['act_jum'] = 0

            if ('img_jum' in model.keys()) and (model['img_jum'] >= int(s_img) and model['img_jum'] <= int(e_img)):
                img_ok = True
            if ('fav_jum' in model.keys()) and (model['fav_jum'] >= int(s_fav) and model['fav_jum'] <= int(e_fav)):
                fav_ok = True
            if ('act_jum' in model.keys()) and (model['act_jum'] >= int(s_act) and model['act_jum'] <= int(e_act)):
                act_ok = True
            # print('ouuuuutt: ', model)

            if img_ok and fav_ok and act_ok:

                output_models.append(model)
            img_ok, fav_ok, act_ok = False, False, False

        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": jsonable_encoder(output_models[:100]), "years": years, "now_year": now_year}
        )

    ###########################################
    # 영상초이
    elif sort_movchoi:

        models = movchoi(db=db, s_date=s_date, e_date=e_date)
        choi_models = jsonable_encoder(models[:])
        filter_models = []

        df = pd.DataFrame(choi_models).groupby(
            ['mcode', 'name']).count().reset_index()

        search_models = df.values.tolist()

        res = sorted(search_models, key=lambda x: x[2], reverse=True)

        for model in res:
            filter_models.append(
                {'mcode': model[0], 'name': model[1], 'count': model[2]})

        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": jsonable_encoder(filter_models[:])}
        )

    ###########################################
    # 프로카운트
    elif sort_proc:
        models = proc(db=db, s_date=s_date, e_date=e_date,
                      gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age, model=model, celeb=celeb)

        print('섹션 구분: ', model, celeb)
        count_models = jsonable_encoder(models[:])
        filter_models = []
        df = pd.DataFrame(count_models).groupby(
            ['mcode', 'name']).count().reset_index()

        search_models = df.values.tolist()
        res = sorted(search_models, key=lambda x: x[2], reverse=True)
        print(res[0])

        for model in res:
            filter_models.append(
                {'mcode': model[0], 'name': model[1], 'count': model[2]})

        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": jsonable_encoder(filter_models[:])}
        )

    ###########################################
    # 순옥스타_최신등록순
    elif sort_register:
        models = order_register(db=db, s_date=s_date, e_date=e_date,
                                gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age, model=model, celeb=celeb)

        print('섹션 구분: ', model, celeb)
        count_models = jsonable_encoder(models[:])

        for model in count_models:
            print(model)

        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": jsonable_encoder(count_models[:])}
        )

    ###########################################
    # 순옥스타_추천순
    elif sort_recommend:
        models = order_recommend(db=db,
                                 gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age)

        filter_models = []
        print(models)
        print('섹션 구분: ', model, celeb)
        count_models = jsonable_encoder(models[:])

        df = pd.DataFrame(count_models).groupby(
            ['mcode', 'name', 'frcode', 'rcode', 'sex', 'age', 'a_3', 'a_6', 'a_12']).sum().reset_index()

        search_models = df.values.tolist()
        print(df)

        res = sorted(search_models, key=lambda x: x[9], reverse=True)

        for model in res:
            print(model)
            filter_models.append(
                {'mcode': model[0], 'name': model[1], 'gender': model[4], 'age': model[5], 'a_3': model[6], 'a_6': model[7], 'a_12': model[8], 'jum1': model[9], 'jum1': model[10]})

        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": jsonable_encoder(filter_models[:])}
        )
