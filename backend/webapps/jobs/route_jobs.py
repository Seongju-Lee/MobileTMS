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
from db.repository.jobs import list_jobs, search_job, list_models, chu_30, movchoi, proc, order_register, order_recommend, order_s_count, order_read
from db.repository.jobs import retrieve_job, create_new_job, order_realtime, models_info
from jinja2 import ModuleLoader
from pyparsing import col
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


# @router.get("/detail/{id}")
# def job_detail(id: int, request: Request, db: Session = Depends(get_db)):
#     job = retrieve_job(id=id, db=db)
#     return templates.TemplateResponse(
#         "jobs/detail.html", {"request": request, "job": job}
#     )


######################
# 날짜, 성별, 연령 등 필터들 예외처리 해놔야 함.
# 필터내용
@ router.get("/filter")
def search_filter(req: Request, s_date: str = '', e_date: str = '', gender_m: str = '', gender_w: str = '',
                  s_img: str = '', e_img: str = '', s_fav: str = '', e_fav: str = '', s_act: str = '', e_act: str = '', s_age: str = '', e_age: str = '', model: str = '', celeb: str = '',
                  sort_thrdays: str = '', sort_movchoi: str = '', sort_proc: str = '', sort_register: str = '', sort_recommend: str = '', sort_s_count: str = '',
                  sort_realtime: str = '', sort_read: str = '', alpha_s_fee: str = '', alpha_e_fee: str = '', s_fee: str = '', e_fee: str = '',
                  query: str = '',
                  db: Session = Depends(get_db)):

    try:
        now_year = datetime.today().year
        years = [i for i in range(now_year-10, 1930, -1)]
        if not (sort_thrdays or sort_movchoi or sort_proc or sort_register or sort_recommend or sort_s_count
                or sort_read or sort_realtime or query):
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
                          gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age, model=model, celeb=celeb, sort_realtime=sort_realtime)

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

        ###########################################
        # 순옥스타_S카운트순
        elif sort_s_count:
            print('aaa')
            models = order_s_count(db=db,
                                   gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age, s_date=s_date, e_date=e_date)

            filter_models = []

            count_models = jsonable_encoder(models[:])
            print(count_models, 'aaa')

            df = pd.DataFrame(count_models).groupby(
                ['mcode', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12']).count().reset_index()

            search_models = df.values.tolist()
            print(df)

            res = sorted(search_models, key=lambda x: x[7], reverse=True)

            for model in res:
                print(model)
                filter_models.append(
                    {'mcode': model[0], 'name': model[1], 'gender': model[2], 'age': model[3], 'a_3': model[4], 'a_6': model[5], 'a_12': model[6]})

            return templates.TemplateResponse(
                "ui-icons.html", {"request": req,
                                  "jobs": jsonable_encoder(filter_models[:])}
            )

        ###########################################
        # 셀럽검색_열람순
        elif sort_read:
            print('aaa')
            models = order_read(db=db,
                                gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age, s_date=s_date, e_date=e_date,
                                e_fee=e_fee, s_fee=s_fee)

            filter_models = []

            count_models = jsonable_encoder(models[:])
            print(count_models, 'aaa')

            df = pd.DataFrame(count_models).groupby(
                ['mcode', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12']).count().reset_index()

            search_models = df.values.tolist()
            print(df)

            res = sorted(search_models, key=lambda x: x[7], reverse=True)

            for model in res:
                print(model)
                filter_models.append(
                    {'mcode': model[0], 'name': model[1], 'gender': model[2], 'age': model[3], 'a_3': model[4], 'a_6': model[5], 'a_12': model[6]})

            return templates.TemplateResponse(
                "ui-icons.html", {"request": req,
                                  "jobs": jsonable_encoder(filter_models[:])}
            )

        ###########################################
        # 셀럽검색_실베스타
        elif sort_realtime:

            model_list = []
            real_time_cf, real_time_activity = order_realtime(db=db,
                                                              gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age,
                                                              e_fee=e_fee, s_fee=s_fee)

            procount = proc(db=db, s_date=s_date, e_date=e_date,
                            gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age, model=model, celeb=celeb, sort_realtime=sort_realtime)

            count_models = jsonable_encoder(real_time_cf[:])
            count_models2 = jsonable_encoder(real_time_activity[:])

            #####################################
            # 계약현황 개수 뽑기
            df_cf = pd.DataFrame(count_models)

            df_cf = df_cf.groupby(
                ['codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12']).count().reset_index()
            # ########################################

            # # ########################################
            # 활동내역 개수 뽑기
            df_activities = pd.DataFrame(count_models2)

            df_activities = df_activities.groupby(
                ['codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12']).count().reset_index()
            # ########################################

            # ########################################
            # # 프로카운트 개수 뽑기
            count_models = jsonable_encoder(procount[:])
            df_proc = pd.DataFrame(count_models).groupby(
                ['codesys', 'rno',  'name', 'sex', 'age', 'a_3', 'a_6', 'a_12']).count().reset_index()
            # ########################################

            df = pd.merge(df_cf, df_activities, how='outer',
                          on=['codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12'])

            df_realTime = pd.merge(df, df_proc, how='outer', on=[
                'codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12'])

            df_realTime = df_realTime.fillna(0)

            search_models = df_realTime.values.tolist()

            for model in search_models:
                sum = model[8]*3 + model[12]*3 + model[10]*1
                model_list.append({'mcode': model[0], 'rno': model[1], 'name': model[2], 'gender': model[3], 'age': model[4], 'a_3': model[5],
                                   'a_6': model[6], 'a_12': model[7], 'cf': model[9], 'activity': model[11], 'proc': model[13], 'sum': sum})

            res = sorted(model_list, key=lambda x: x['sum'], reverse=True)
            for model in res:
                print(model)

            return templates.TemplateResponse(
                "ui-icons.html", {"request": req,
                                  "jobs": jsonable_encoder(res[:])}
            )

        elif query:
            models = search_job(db=db, query=query)

            models_search = jsonable_encoder(models[:])
            print(models_search)

            return templates.TemplateResponse(
                "ui-icons.html", {"request": req,
                                  "jobs": models_search}
            )

    except:
        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "no_result": '만족하는 결과가 없습니다.',
                              'alert': '검색 필터가 누락되었는 지 확인 해주세요'}
        )

######################
# 세부정보


@ router.get("/detail/{rno}")
def model_info(req: Request, rno: int, db: Session = Depends(get_db)):

    try:
        print('세부 정보 페이지 접속..', rno)
        info = models_info(db=db, rno=rno)
        print(info)
        print(jsonable_encoder(info[0]))
        # 세부정보
        # rno를 api서버로 가져감. rno에 해당되는 Yeon.codesys를 조회함.
        # 여기 없으면 People.codesys의 no으로 인식하고, rno와 일치하는 no에 해당하는People.codesys를 조회함.
        # Yeon에서 가져온 경우에는 연예인 세부정보를 뿌려주고,
        # People에서 가져온 경우에는 모델 세부정보를 뿌려준다.
        return templates.TemplateResponse(
            "page-user.html", {"request": req,
                               'item': jsonable_encoder(info[0])}
        )
    except:
        pass
