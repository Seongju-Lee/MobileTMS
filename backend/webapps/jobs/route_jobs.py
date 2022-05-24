from datetime import datetime
from multiprocessing.dummy import JoinableQueue
from pyexpat import model
from re import A
from statistics import mode
from time import time
import turtle
from black import out
from fastapi import APIRouter, Depends
from fastapi import Request, status, responses, Response, requests
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.repository.jobs import list_jobs, search_job, list_models, chu_30, movchoi, proc, order_register, order_recommend, order_s_count, order_read, search_celeb
from db.repository.jobs import retrieve_job, create_new_job, order_realtime, models_info
from jinja2 import ModuleLoader
from numpy import mod
from pyparsing import col
from sqlalchemy import JSON, String,  null
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.users import User
from apis.version1.route_login import get_current_user_from_token
from webapps.jobs.forms import JobCreateForm
from schemas.jobs import JobCreate
from typing import Optional
from fastapi.encoders import jsonable_encoder
from striprtf.striprtf import rtf_to_text

import json
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


######################
# 날짜, 성별, 연령 등 필터들 예외처리 해놔야 함.
# 필터내용
@ router.get("/filter")
def search_filter(req: Request, s_date: str = '', e_date: str = '', gender_m: str = '', gender_w: str = '',
                  s_img: str = '', e_img: str = '', s_fav: str = '', e_fav: str = '', s_act: str = '', e_act: str = '', s_age: str = '',hidden_s_age:str='', hidden_e_age:str='', hidden_alpha_fee:str='', hidden_celeb_fee:str='', hidden_celeb_fee_month:str='',
                  hidden_celeb_section: str='',
                  e_age: str = '', chk_model: str = '', chk_celeb: str = '',
                  sort_thrdays: str = '', sort_movchoi: str = '', sort_proc: str = '', sort_register: str = '', sort_recommend: str = '', sort_s_count: str = '',
                  sort_realtime: str = '', sort_read: str = '', alpha_s_fee: str = '', alpha_e_fee: str = '', s_fee: str = '', e_fee: str = '',
                  query: str = '', name: str = '', coname: str = '', manager: str = '', tel: str = '', chk_age: str = '', alpha_fees: str = '',
                  db: Session = Depends(get_db)):

    # try:
    now_year = datetime.today().year
    years = [i for i in range(now_year-10, 1930, -1)]
    ll = []
    search_ages = [] # 설정된 나이 구간 저장.
    ll.append(alpha_fees)
    if not (sort_thrdays or sort_movchoi or sort_proc or sort_register or sort_recommend or sort_s_count
            or sort_read or sort_realtime or name or coname or manager or tel):
        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "years": years,  "now_year": now_year}
        )

    hidden_s_age = hidden_s_age.split(',')
    hidden_e_age = hidden_e_age.split(',')

    print(hidden_e_age)
    for i in range(len(hidden_e_age)):
        search_ages.append([int(hidden_s_age[i].split('(')[1].split(')')[0]), int(hidden_e_age[i].split('(')[1].split(')')[0])])

    print('알파모델료 TEST: ', hidden_alpha_fee)


    ###########################################
    # 추천 30일
    if sort_thrdays:
        models = chu_30(db=db, chu_act=s_act,
                        chu_fav=s_fav, chu_img=s_img, gender_m=gender_m, gender_w=gender_w, search_ages=search_ages, hidden_alpha_fee=hidden_alpha_fee)

        img_ok, fav_ok, act_ok = False, False, False
        chu_models = jsonable_encoder(models[:])
        res_models = []
        i = 0
        # print(chu_models)
        df = pd.DataFrame(chu_models).groupby(
            ['mcode', 'gubun', 'name', 'jum', 'mfee',  'sex', 'coname', 'height', 'age', 'isyeon']).sum().reset_index()

        search_models = df.values.tolist()
        # print(search_models)
        filter_models = []
        output_models = []
        for model in (search_models):
            print(': ', model)
            if model[1] == 'act':
                res_models.append(
                    {'mcode': model[0], 'gubun': model[1], 'name': model[2], 'act_jum': model[3],
                    'mfee':model[4], 'gender':model[5], 'coname':model[6],
                    'height':model[7],'age':model[8], 'isyeon':model[9]})
            elif model[1] == 'fav':
                res_models.append(
                    {'mcode': model[0], 'gubun': model[1], 'name': model[2], 'fav_jum': model[3],
                    'mfee':model[4], 'gender':model[5], 'coname':model[6],
                    'height':model[7],'age':model[8], 'isyeon':model[9]})
            elif model[1] == 'img':
                res_models.append(
                    {'mcode': model[0], 'gubun': model[1], 'name': model[2], 'img_jum': model[3],
                    'mfee':model[4], 'gender':model[5], 'coname':model[6],
                    'height':model[7],'age':model[8], 'isyeon':model[9]})

            if len(res_models) != i:
               
                if res_models[i]['mcode'] == res_models[i-1]['mcode']:

                    res_models[i].update(res_models[i-1])
                else:
                    filter_models.append(res_models[i-1])

                i += 1

        filter_models.append(res_models[i-1])  # 마지막 모델 추가


        try:

            with open("model.json", 'r', encoding='utf-8') as json_file:
                aa = json.load(json_file)
                for job in filter_models:
                    if not job['mfee'] == '':
                        job['mfee'] = aa['model_fee'][job['mfee']]
            # print('안녕!!ㅎㅎ: ', res_models)
        except:
            print('일치하는 모델료가 json파일에 없음.')
            pass

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

        for model in output_models:
            model['sum'] = model['img_jum'] + model['fav_jum'] + model['act_jum']
            
        res = sorted(output_models, key=lambda x: x['sum'], reverse=True)

        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": res, "years": years, "now_year": now_year}
        )

    ###########################################


    ###########################################
    # 영상초이
    elif sort_movchoi:

        print(search_ages)
        models = movchoi(db=db, gender_w=gender_w, gender_m=gender_m, s_date=s_date, e_date=e_date, search_ages = search_ages, hidden_alpha_fee=hidden_alpha_fee)
        choi_models = jsonable_encoder(models[:])
        res_models = []

        df = pd.DataFrame(choi_models).groupby(
            ['mcode', 'name', 'age', 'mfee', 'sex', 'coname', 'height', 'isyeon']).count().reset_index()

        search_models = df.values.tolist()
        print(search_models)

        res = sorted(search_models, key=lambda x: x[8], reverse=True)

        for model in res:
            print(model)
            res_models.append(
                {'mcode': model[0], 'name': model[1], 'age': model[2], 'mfee':model[3], 'gender':model[4], 'coname':model[5], 'height':model[6],'isyeon':model[8] ,'count': model[len(model)-1]})

        try:

            with open("model.json", 'r', encoding='utf-8') as json_file:
                aa = json.load(json_file)
                for job in res_models:
                    if not job['mfee'] == '':
                        job['mfee'] = aa['model_fee'][job['mfee']]
            # print('안녕!!ㅎㅎ: ', res_models)
        except:
            print('일치하는 모델료가 json파일에 없음.')
            pass

        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": res_models[:],
                              "years": years,  "now_year": now_year}
        )
    ###########################################


    ###########################################
    # 프로카운트
    elif sort_proc:
        models, gubun = proc(db=db, s_date=s_date, e_date=e_date, hidden_alpha_fee=hidden_alpha_fee,
                             gender_w=gender_w, gender_m=gender_m,  search_ages = search_ages, model=chk_model, celeb=chk_celeb, sort_realtime=sort_realtime)

        count_models = jsonable_encoder(models[:])
        filter_models = []
        if gubun == 'model':
            df = pd.DataFrame(count_models).groupby(
                ['mcode', 'name', 'sex', 'age', 'coname', 'mfee', 'height']).count().reset_index()

            search_models = df.values.tolist()
            res = sorted(search_models, key=lambda x: x[2], reverse=True)

            for model in res:
                filter_models.append(
                    {'mcode': model[0], 'name': model[1], 'gender': model[2], 'age': model[3], 'coname': model[4], 'mfee': model[5],  'height': model[6], 'isyeon':model[8], 'count': model[len(model)-1]})

            print('Test: ', jsonable_encoder(filter_models[:])[0])
            res_models = jsonable_encoder(filter_models[:])
            try:

                with open("model.json", 'r', encoding='utf-8') as json_file:
                    aa = json.load(json_file)
                    for job in res_models:
                        if not job['mfee'] == '':
                            job['mfee'] = aa['model_fee'][job['mfee']]
                # print('안녕!!ㅎㅎ: ', res_models)
            except:
                print('일치하는 모델료가 json파일에 없음.')
                pass
            return templates.TemplateResponse(
                "ui-icons.html", {"request": req,
                                  "jobs": res_models,
                                  "gubun": gubun,
                                  "years": years,  "now_year": now_year}
            )
    ####################33333##################


    ###########################################
    # 순옥스타_최신등록순
    elif sort_register:

        print(hidden_celeb_section)
        models = order_register(db=db, s_date=s_date, e_date=e_date, hidden_celeb_fee= hidden_celeb_fee, hidden_celeb_fee_month= hidden_celeb_fee_month, hidden_celeb_section=hidden_celeb_section,
                                gender_w=gender_w, gender_m=gender_m, search_ages = search_ages)

        count_models = jsonable_encoder(models[:])

    
        try:

            with open("model.json", 'r', encoding='utf-8') as json_file:
                aa = json.load(json_file)
                for job in count_models:
                    print(job)
                    if not job['mfee'] == '':
                        if not  job['isyeon'] == 'V':
                            job['mfee'] = aa['model_fee'][job['mfee']]
                    if job['a_3'] == 0:
                        job['a_3'] = 'X'
                    if job['a_6'] == 0:
                        job['a_6'] = 'X'
                    if job['a_12'] == 0:
                        job['a_12'] = 'X'
                    
            
        except:
            print('일치하는 모델료가 json파일에 없음.')
            pass
        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": count_models,
                              "years": years,  "now_year": now_year}
        )
    ###########################################


    ###########################################
    # 순옥스타_추천순
    elif sort_recommend:
        models = order_recommend(db=db,
                                 gender_w=gender_w, gender_m=gender_m, search_ages=search_ages, hidden_celeb_fee=hidden_celeb_fee,
                                 hidden_celeb_fee_month=hidden_celeb_fee_month,  hidden_celeb_section= hidden_celeb_section)

        filter_models = []
        print(models)
        print('섹션 구분: ', chk_model, chk_celeb)
        count_models = jsonable_encoder(models[:])
        print(count_models)
        df = pd.DataFrame(count_models).groupby(
            ['mcode', 'name', 'frcode', 'rcode', 'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon', 'height', 'coname', 'mfee']).sum().reset_index()

        search_models = df.values.tolist()
        for model in search_models:
            print('검색모델: ', model)

        res = sorted(search_models, key=lambda x: x[13], reverse=True)

        for model in res:
            print(model)
            filter_models.append(
                {'mcode': model[0], 'name': model[1], 'gender': model[4], 'age': model[5], 'a_3': model[6], 'a_6': model[7], 'a_12': model[8], 'isyeon': model[9], 'jum1': model[13], 'jum1': model[14]})

        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": jsonable_encoder(filter_models[:]),
                              "years": years,  "now_year": now_year}
        )
    ###########################################


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
                              "jobs": jsonable_encoder(filter_models[:]),
                              "years": years,  "now_year": now_year}
        )
    ###########################################


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
                              "jobs": jsonable_encoder(filter_models[:]),
                              "years": years,  "now_year": now_year}
        )
    ###########################################


    ###########################################
    # 셀럽검색_실베스타
    elif sort_realtime:
        model_list = []
        real_time_cf, real_time_activity = order_realtime(db=db,
                                                          gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age,
                                                          e_fee=e_fee, s_fee=s_fee)

        procount, gubun = proc(db=db, s_date=s_date, e_date=e_date,
                               gender_w=gender_w, gender_m=gender_m, s_age=s_age, e_age=e_age, model=chk_model, celeb=chk_celeb, sort_realtime=sort_realtime)

        count_models = jsonable_encoder(real_time_cf[:])
        count_models2 = jsonable_encoder(real_time_activity[:])

        #####################################
        # 계약현황 개수 뽑기
        df_cf = pd.DataFrame(count_models)

        df_cf = df_cf.groupby(
            ['codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon']).count().reset_index()
        # ########################################

        # # ########################################
        # 활동내역 개수 뽑기
        df_activities = pd.DataFrame(count_models2)

        df_activities = df_activities.groupby(
            ['codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon']).count().reset_index()
        # ########################################

        # ########################################
        # # 프로카운트 개수 뽑기
        count_models = jsonable_encoder(procount[:])
        df_proc = pd.DataFrame(count_models).groupby(
            ['codesys', 'rno',  'name', 'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon']).count().reset_index()

        # ########################################

        df = pd.merge(df_cf, df_activities, how='outer',
                      on=['codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12',  'isyeon'])

        df_realTime = pd.merge(df, df_proc, how='outer', on=[
            'codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon'])

        df_realTime = df_realTime.fillna(0)

        search_models = df_realTime.values.tolist()
        print('aaaadddd: ', search_models)
        for model in search_models:

            sum = model[9]*3 + model[13]*3 + model[11]*1
            model_list.append({'mcode': model[0], 'rno': model[1], 'name': model[2], 'gender': model[3], 'age': model[4], 'a_3': model[5],
                               'a_6': model[6], 'a_12': model[7], 'isyeon': model[8], 'cf': model[9], 'activity': model[11], 'proc': model[13], 'sum': sum})

        res = sorted(model_list, key=lambda x: x['sum'], reverse=True)
        # for model in res:
        #     print(model)

        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "jobs": jsonable_encoder(res[:]),
                              "years": years,  "now_year": now_year}
        )
    ########################################


    ########################################
    #  # 단순검색
    elif name or coname or tel or manager:

        models = search_job(
            db=db, name=name, coname=coname, tel=tel, manager=manager)

        models_search = jsonable_encoder(models[:])
        print(models_search)
        celebs, kmodels = [], []
        for model in models_search:
            if model['isyeon'] == 'V':
                celeb = search_celeb(db=db, mcode=model['mcode'])
                search_celebs = jsonable_encoder(celeb[:])
                celebs.append(search_celebs[0])
            else:
                kmodels.append(model)

        jobs = celebs + kmodels
        print('최종 검색 본: ', jobs)

        try:

            with open("model.json", 'r', encoding='utf-8') as json_file:
                aa = json.load(json_file)
                for job in jobs:
                    if not job['mfee'] == '':
                        job['mfee'] = aa['model_fee'][job['mfee']]
            print(jobs)
        except:
            print('일치하는 모델료가 json파일에 없음.')
            pass

        # gubun 이라는 키가 들어가 있는 models_search를 ui-icons로 보냄.
        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "kmodels": kmodels,
                              "jobs": jobs,
                              "years": years,  "now_year": now_year}
        )
    ########################################


    # except:
    #     return templates.TemplateResponse(
    #         "ui-icons.html", {"request": req,
    #                           "no_result": '만족하는 결과가 없습니다.',
    #                           'alert': '검색 필터가 누락되었는 지 확인 해주세요',
    #                           "years": years,  "now_year": now_year}
    #     )



######################
# 세부정보
@ router.get("/detail/{codesys}")
def model_info(req: Request, codesys: str = '', db: Session = Depends(get_db)):

    try:
        print('세부 정보 페이지 접속..', codesys)
        info, activities, call_memo, token = models_info(
            db=db, codesys=codesys)

        if not token == 123:
            res = jsonable_encoder((info[:]))
            calls = jsonable_encoder((call_memo[:]))
            activity = jsonable_encoder((activities[:]))
            res_model = jsonable_encoder((info[0]))
            celeb_cf = []
            celeb_activity = []
            celeb_calls = []
            res_model['point2'] = rtf_to_text(res_model['point2'])
            print('22222222222222222222222: ', res_model)

            i = 0
            for model in res:
                res[i]['point2'] = rtf_to_text(model['point2'])

                i += 1
            for m in res:

                celeb_cf.append({'brand': m['brand'], 'poom': m['poom'],
                                'imonth': m['imonth'], 'fee': m['fee'], 'dstart': m['dstart'], 'dend': m['dend'], 'indefin': m['indefin'], 'nation': m['nation'], 'writer': m['writer'], 'wrdate': m['wrdate']})

            for m in activity:
                # print(m)
                celeb_activity.append({'gubun': m['drgubun'], 'gubun2': m['drgubun2'], 'title': m['title'], 'dstart': m['dstart'], 'dend': m['dend'], 'writer': m['writer'],
                                       'wrdate': m['wrdate']})
            print('qqqqqq: ', calls)
            for call in calls:

                try:
                    celeb_calls.append(
                        {'title': call['title'], 'memo': call['memo'].split('\r\n'), 'rcode': call['rcode']})
                except:
                    pass

            res_model['point_str'] = res_model['point2'].split('\n')

            return templates.TemplateResponse(
                "page-user.html", {"request": req,
                                   'item': res_model,
                                   'celeb_cf': celeb_cf,
                                   'celeb_activity': celeb_activity,
                                   'celeb_calls': celeb_calls}
            )

        else:

            calls = jsonable_encoder((call_memo[:]))
            model_calls = []
            res_model = info
            res_model['point2'] = rtf_to_text(res_model['point2'])

            res_model['point_str'] = res_model['point2'].split('\n')
            print('ppppp_kmodel: ', jsonable_encoder(activities[:]))

            try:

                with open("model.json", 'r', encoding='utf-8') as json_file:
                    aa = json.load(json_file)
                    res_model['mfee'] = aa['model_fee'][res_model['mfee']]
                    # print(res_model)
            except:
                print('일치하는 모델료가 json파일에 없음.')

            print('광고이력 개수: ', len(jsonable_encoder(activities[:])))

            try:
                for call in calls:
                    model_calls.append(
                        {'title': call['title'], 'memo': call['memo'].split('\r\n'), 'rcode': call['rcode']})

                print('model_통화메모입니다.: ', model_calls)
            except:
                pass

            # 모델 전용 세부 페이지로 이동
            return templates.TemplateResponse(
                "page-user_model.html", {"request": req,
                                         'item': res_model,
                                         'activities': jsonable_encoder(activities[:]),
                                         "model_calls": model_calls}
            )
        
    except:
        print('에러 발생: ')
        pass
