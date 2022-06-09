from dataclasses import dataclass
from datetime import datetime, timedelta
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
from db.repository.jobs import retrieve_job, create_new_job, order_realtime, models_info, proc_celeb, img_mov_info, cf_mov_info, act_mov_info
from jinja2 import ModuleLoader
from numpy import min_scalar_type, mod
from pyparsing import col
from sqlalchemy import JSON, String,  null, true
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.users import User
from apis.version1.route_login import get_current_user_from_token
from webapps.jobs.forms import JobCreateForm
from schemas.jobs import JobCreate
from typing import Optional
from fastapi.encoders import jsonable_encoder
from striprtf.striprtf import rtf_to_text
from starlette.responses import RedirectResponse

import json
import pandas as pd

templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]

    try:
        
        token: str = request.cookies.get("access_token")

        print('token입니다. ', token)
        if token is None:
            return RedirectResponse('/login')
        
        else:

            return templates.TemplateResponse(
                "index.html", {"request": request,
                            "years": years,  "now_year": now_year}
            )

    except:
        print('?')

@router.post("/")
def home(request: Request, db: Session = Depends(get_db)):
    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]

    # print(now_time, 'aaaaaaaaaaaa')
    try:
        
        # if datetime.now() > (access_time + timedelta(minutes=1)):
        #     request.cookies.__delitem__("access_token")
        
        token: str = request.cookies.get("access_token")

        print('token입니다. ', token)
        if token is None:
            return RedirectResponse('/login')
        
        else:

            return templates.TemplateResponse(
                "index.html", {"request": request,
                            "years": years,  "now_year": now_year}
            )

    except:
        print('?')

# @router.get("/login")
# def home(request: Request, db: Session = Depends(get_db)):

#     now_year = datetime.today().year
#     years = [i for i in range(now_year-10, 1930, -1)]

#     return templates.TemplateResponse(
#         "login.html", {"request": request,
#                        "years": years,  "now_year": now_year}
#     )


######################
# 날짜, 성별, 연령 등 필터들 예외처리 해놔야 함.
# 필터내용
@ router.get("/filter")
def search_filter(req: Request, s_date: str = '', e_date: str = '', gender_m: str = '', gender_w: str = '', model_filter: str ='', filter_celeb: str ='',
                  s_img: str = '', e_img: str = '', s_fav: str = '', e_fav: str = '', s_act: str = '', e_act: str = '', s_age: str = '', hidden_alpha_fee:str='', hidden_celeb_fee:str='', hidden_celeb_fee_month:str='',
                  hidden_celeb_section: str='',
                  e_age: str = '', chk_model: str = '', chk_celeb: str = '',
                  query: str = '', name: str = '', coname: str = '', manager: str = '', tel: str = '', chk_age: str = '', alpha_fees: str = '',
                  hidden_echar: str = '', hidden_rchar: str = '', btn_img: str='', btn_fav: str='', btn_act: str='', hidden_score : str='',
                  db: Session = Depends(get_db)):


    ###########3 셀럽 선택 시, 모델 관련 체크 다 지우고, 모델 선택 시,, 셀럽 
    # try:

    token: str = req.cookies.get("access_token")

    print('token입니다. ', token)
    if token is None:
        return RedirectResponse('/login')
    
    else:
        pass
        # return templates.TemplateResponse(
        #     "index.html", {"request": request,
        #                 "years": years,  "now_year": now_year}
        # )

    if chk_celeb == '':
        filter_celeb = ''

    elif chk_model == '':
        model_filter = ''

    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]
    ll = []
    search_ages = [] # 설정된 나이 구간 저장.
    ll.append(alpha_fees)
    if not (model_filter or filter_celeb or name or coname or manager or tel ):
        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "years": years,  "now_year": now_year}
        )

    # hidden_s_age = hidden_s_age.split(',')
    # hidden_e_age = hidden_e_age.split(',')

    # print(hidden_e_age)
    # if (not hidden_s_age[0] == '') and (not hidden_e_age[0] == ''):
    #     for i in range(len(hidden_e_age)):
    #         search_ages.append([int(hidden_s_age[i].split('(')[1].split(')')[0]), int(hidden_e_age[i].split('(')[1].split(')')[0])])


    search_ages.append([s_age, e_age])
    print('연령 TEST: ', search_ages)
    print('알파모델료 TEST: ', hidden_alpha_fee)



   


    try:
        ###########################################
        # 추천 30일
        if model_filter == 'thrdays':
            models = chu_30(db=db, chu_act=s_act,
                            chu_fav=s_fav, chu_img=s_img, gender_m=gender_m, gender_w=gender_w,
                            search_ages=search_ages, hidden_alpha_fee=hidden_alpha_fee,
                            hidden_echar=hidden_echar, hidden_rchar=hidden_rchar)

            img_ok, fav_ok, act_ok = False, False, False
            chu_models = jsonable_encoder(models[:])
            res_models = []
            
            i = 0
            df = pd.DataFrame(chu_models).groupby(
                ['mcode', 'gubun', 'name',  'mfee',  'sex', 'coname', 'height', 'age', 'isyeon'])['jum'].sum().reset_index()

            search_models = df.values.tolist()
            filter_models = []
            output_models = []

                
            for model in (search_models):
                
                res_models.append(
                    {'mcode': model[0], 'gubun': model[1], 'name': model[2],
                    'mfee':model[3], 'gender':model[4], 'coname':model[5],
                    'height':model[6],'age':model[7], 'isyeon':model[8], 'jum': model[9]})


            

            df_res = pd.DataFrame(res_models).groupby(
                ['mcode', 'gubun', 'name', 'mfee',  'gender', 'coname', 'height', 'age', 'isyeon'])['jum'].apply(list).reset_index(name='sum')

            df_to_list = df_res.values.tolist()

            
            j=0
            for model in df_to_list:
                
                tmp = 0
                for i in range(len(model[9])):
                    tmp += model[9][i]
                model[9] = tmp 
                df_to_list[j] = {'mcode': model[0], 'gubun': model[1], 'name': model[2],
                        'mfee':model[3], 'gender':model[4], 'coname':model[5],
                        'height':model[6],'age':model[7], 'isyeon':model[8], 'jum':model[9]}
                j += 1

            for model in (df_to_list):
                # print('냐냐냐냐냐니: ', model)
                if model['gubun'] == 'act':
                    model['act_jum'] = model['jum']
                elif model['gubun'] == 'fav':
                    model['fav_jum'] = model['jum']
                elif model['gubun'] == 'img':
                    model['img_jum'] = model['jum']

            

            for i in range(len(df_to_list)):
                try:
                    if i == 0:
                        pass
                    
                    elif df_to_list[i]['mcode'] == df_to_list[i-1]['mcode']:
                        
                        df_to_list[i].update(df_to_list[i-1])
                    else:
                        filter_models.append(df_to_list[i-1])
                except:
                    pass
                

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


            print('dkkkkkkkkkkk: ', hidden_score)

            hidden_scores = hidden_score.split(',')

            for model in filter_models:
                

                
                if not 'img_jum' in model.keys():
                    model['img_jum'] = 0
                if not 'fav_jum' in model.keys():
                    model['fav_jum'] = 0
                if not 'act_jum' in model.keys():
                    model['act_jum'] = 0



                if s_img == '0' and e_img == '0':
                    model['img_jum'] = 0
                if s_fav == '0' and e_fav == '0':
                    model['fav_jum'] = 0
                if (s_act == '0') and (e_act == '0'):
                    model['act_jum'] = 0

                if 'chk_img' in hidden_scores:
                    if ('img_jum' in model.keys()) and (model['img_jum'] >= int(s_img) and model['img_jum'] <= int(e_img)):
                        img_ok = True
                if 'chk_fav' in hidden_scores:
                    if ('fav_jum' in model.keys()) and (model['fav_jum'] >= int(s_fav) and model['fav_jum'] <= int(e_fav)):
                        fav_ok = True
                if 'chk_act' in hidden_scores:
                    if ('act_jum' in model.keys()) and (model['act_jum'] >= int(s_act) and model['act_jum'] <= int(e_act)):
                        act_ok = True

                if img_ok or fav_ok or act_ok:
                   
                    output_models.append(model)
                img_ok, fav_ok, act_ok = False, False, False


          
                model['sum'] = model['img_jum'] + model['fav_jum'] + model['act_jum']
                
                
            res = sorted(output_models, key=lambda x: x['sum'], reverse=True)
            
                
            return templates.TemplateResponse(
                "ui-icons.html", {"request": req,
                                "jobs": res, "years": years, "now_year": now_year}
            )

        ###########################################


        ###########################################
        # 영상초이
        elif model_filter == 'movchoi':

            # print(search_ages)
            models = movchoi(db=db, gender_w=gender_w, gender_m=gender_m, s_date=s_date, e_date=e_date, search_ages = search_ages,
            hidden_alpha_fee=hidden_alpha_fee , hidden_echar=hidden_echar, hidden_rchar=hidden_rchar)

            choi_models = jsonable_encoder(models[:])
            res_models = []

            df = pd.DataFrame(choi_models).groupby(
                ['mcode', 'name', 'age', 'mfee', 'sex', 'coname', 'height', 'isyeon']).count().reset_index()

            search_models = df.values.tolist()
            # print(search_models)

            
            res = sorted(search_models, key=lambda x: x[8], reverse=True)


            for model in res[:400]:
                # print(model)
                res_models.append(
                    {'mcode': model[0], 'name': model[1], 'age': model[2], 'mfee':model[3], 'gender':model[4], 'coname':model[5], 'height':model[6],'isyeon':model[8] ,'count': model[len(model)-1]})

        
            try:

                with open("model.json", 'r', encoding='utf-8') as json_file:
                    aa = json.load(json_file)
                    for job in res_models:
                        if not job['mfee'] == '':
                            job['mfee'] = aa['model_fee'][job['mfee']]
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
        elif model_filter == 'proc':
            models, gubun = proc(db=db, s_date=s_date, e_date=e_date, hidden_alpha_fee=hidden_alpha_fee,
                                gender_w=gender_w, gender_m=gender_m,  search_ages = search_ages, model=chk_model, celeb=chk_celeb,
                                hidden_echar=hidden_echar, hidden_rchar=hidden_rchar)

            count_models = jsonable_encoder(models[:])
            filter_models = []
            if gubun == 'model':
                df = pd.DataFrame(count_models).groupby(
                    ['mcode', 'name', 'sex', 'age', 'coname', 'mfee', 'height']).count().reset_index()

                search_models = df.values.tolist()
                res = sorted(search_models, key=lambda x: x[10], reverse=True)

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
        elif filter_celeb == 'order_register':

            print(hidden_celeb_section)
            models = order_register(db=db,  hidden_celeb_fee= hidden_celeb_fee, hidden_celeb_fee_month= hidden_celeb_fee_month, hidden_celeb_section=hidden_celeb_section,
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
        elif filter_celeb == 'recommend':
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
                    {'mcode': model[0], 'name': model[1], 'gender': model[4], 'age': model[5], 'a_3': model[6], 'a_6': model[7], 'a_12': model[8], 'isyeon': model[9],'height': model[10], 'coname': model[11], 'mfee': model[12], 'jum1': model[13], 'jum1': model[14]})

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
                                "jobs": jsonable_encoder(filter_models[:]),
                                "years": years,  "now_year": now_year}
            )
        ###########################################


        ###########################################
        # 순옥스타_S카운트순
        elif filter_celeb == 's_count':
            models = order_s_count(db=db,
                                gender_w=gender_w, gender_m=gender_m, search_ages=search_ages, hidden_celeb_fee=hidden_celeb_fee, hidden_celeb_fee_month=hidden_celeb_fee_month ,
                                hidden_celeb_section=hidden_celeb_section,s_date=s_date, e_date=e_date)

            filter_models = []

            count_models = jsonable_encoder(models[:])
            

            df = pd.DataFrame(count_models).groupby(
                ['mcode', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon', 'height', 'coname', 'mfee']).count().reset_index()

            search_models = df.values.tolist()
            print(df)
            res = sorted(search_models, key=lambda x: x[11], reverse=True)
            # search_models

            for m in res[:10]:
                print(m)
            for model in res:
                filter_models.append(
                    {'mcode': model[0], 'name': model[1], 'gender': model[2], 'age': model[3], 'a_3': model[4], 'a_6': model[5], 'a_12': model[6],
                    'isyeon': model[7], 'height': model[8], 'coname':model[9], 'mfee':model[10]})


            # for model in filter_models[:10]:
            #     print('ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ: ', model)

            try:

                with open("model.json", 'r', encoding='utf-8') as json_file:
                    aa = json.load(json_file)
                    for job in filter_models:
                        # print(job)
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
                                "jobs": filter_models,
                                "years": years,  "now_year": now_year}
            )
        ###########################################


        ###########################################
        # 셀럽검색_열람순
        elif filter_celeb == 'read':
            print('aaa')
            models = order_read(db=db,
                                gender_w=gender_w, gender_m=gender_m, search_ages=search_ages, s_date=s_date, e_date=e_date,
                                hidden_celeb_fee=hidden_celeb_fee, hidden_celeb_fee_month=hidden_celeb_fee_month, hidden_celeb_section=hidden_celeb_section)
            filter_models = []

            count_models = jsonable_encoder(models[:])
            # print(count_models, 'aaa')
            df = pd.DataFrame(count_models).groupby(
                ['mcode', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon', 'height', 'coname', 'mfee']).count().reset_index()

            search_models = df.values.tolist()

            res = sorted(search_models, key=lambda x: x[11], reverse=True)

            for model in res:
                # print(model)
                filter_models.append(
                    {'mcode': model[0], 'name': model[1], 'gender': model[2], 'age': model[3], 'a_3': model[4], 'a_6': model[5], 'a_12': model[6],
                    'isyeon': model[7], 'height': model[8], 'coname':model[9],'mfee':model[10]})


            try:

                with open("model.json", 'r', encoding='utf-8') as json_file:
                    aa = json.load(json_file)
                    for job in filter_models:
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
                                "jobs": filter_models,
                                "years": years,  "now_year": now_year}
            )
        ###########################################


        ###########################################
        # 셀럽검색_실베스타
        elif filter_celeb == 'order_realtime':
            model_list = []
            real_time_cf, real_time_activity = order_realtime(db=db,
                                                            gender_w=gender_w, gender_m=gender_m, search_ages=search_ages,
                                                            hidden_celeb_fee=hidden_celeb_fee, hidden_celeb_fee_month=hidden_celeb_fee_month, hidden_celeb_section=hidden_celeb_section)
            procount = proc_celeb(db=db, gender_w=gender_w, gender_m=gender_m, search_ages=search_ages, hidden_celeb_fee=hidden_celeb_fee, hidden_celeb_fee_month=hidden_celeb_fee_month,
                                    hidden_celeb_section=hidden_celeb_section, s_date=s_date, e_date=e_date)

            count_models = jsonable_encoder(real_time_cf[:])
            count_models2 = jsonable_encoder(real_time_activity[:])


            #####################################
            # 계약현황 개수 뽑기
            df_cf = pd.DataFrame(count_models)

            print('erai sibal: ', df_cf)

            df_cf = df_cf.groupby(
                ['codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon', 'height', 'mfee', 'coname']).count().reset_index()
            # ########################################

            # # ########################################
            # 활동내역 개수 뽑기
            df_activities = pd.DataFrame(count_models2)

            df_activities = df_activities.groupby(
                ['codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon', 'height', 'mfee', 'coname']).count().reset_index()
            # ########################################

            # ########################################
            # # 프로카운트 개수 뽑기
            count_models = jsonable_encoder(procount[:])
            df_proc = pd.DataFrame(count_models).groupby(
                ['codesys', 'rno',  'name', 'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon', 'height', 'mfee', 'coname']).count().reset_index()

            # ########################################

            df = pd.merge(df_cf, df_activities, how='outer',
                        on=['codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12',  'isyeon', 'height', 'mfee', 'coname'])

            df_realTime = pd.merge(df, df_proc, how='outer', on=[
                'codesys', 'rno', 'name',  'sex', 'age', 'a_3', 'a_6', 'a_12', 'isyeon', 'height', 'mfee', 'coname'])

            df_realTime = df_realTime.fillna(0)

            search_models = df_realTime.values.tolist()
            
            for model in search_models:
                sum = model[13]*3 + model[15]*1 + model[17]*3
                model_list.append({'mcode': model[0], 'rno': model[1], 'name': model[2], 'gender': model[3], 'age': model[4], 'a_3': model[5],
                                'a_6': model[6], 'a_12': model[7], 'isyeon': model[8], 'height': model[9],'mfee':model[10],'coname':model[11], 'cf': model[13], 'activity': model[15], 'proc': model[17], 'sum': sum})

            res = sorted(model_list, key=lambda x: x['sum'], reverse=True)
            for model in res[:10]:
                print(model)


            try:

                with open("model.json", 'r', encoding='utf-8') as json_file:
                    aa = json.load(json_file)
                    for job in res:
                        # print(job)
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


    except:
        return templates.TemplateResponse(
            "ui-icons.html", {"request": req,
                              "no_result": '만족하는 결과가 없습니다.',
                              "years": years,  "now_year": now_year}
        )




######################
# 세부정보
@ router.get("/detail/{codesys}")
def model_info(req: Request, codesys: str = '', db: Session = Depends(get_db)):



    try:
        
        token: str = req.cookies.get("access_token")

        print('token입니다. ', token)
        if token is None:
            return RedirectResponse('/login')
       

    except:
        print('get token error')

    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]

    # try:
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

        i = 0
        for model in res:
            res[i]['point2'] = rtf_to_text(model['point2'])

            i += 1
        for m in res:

            celeb_cf.append({'brand': m['brand'], 'poom': m['poom'],
                            'imonth': m['imonth'], 'fee': m['fee'], 'dstart': m['dstart'], 'dend': m['dend'], 'indefin': m['indefin'], 'nation': m['nation'], 'writer': m['writer'], 'wrdate': m['wrdate']})

        for m in activity:
            celeb_activity.append({'gubun': m['drgubun'], 'gubun2': m['drgubun2'], 'title': m['title'], 'dstart': m['dstart'], 'dend': m['dend'], 'writer': m['writer'],
                                    'wrdate': m['wrdate']})
        
        try:
            for call in calls:

                celeb_calls.append(
                    {'title': call['title'], 'memo': call['memo'].split('\r\n'), 'rcode': call['rcode']})

            celeb_calls = list(reversed(celeb_calls))
            print(celeb_calls)
        except:
            print('셀럽 통화메모 정렬 에러발생')

        res_model['point_str'] = res_model['point2'].split('\n')

        return templates.TemplateResponse(
            "page-user.html", {"request": req,
                                'item': res_model,
                                'celeb_cf': celeb_cf,
                                'celeb_activity': celeb_activity,
                                'celeb_calls': celeb_calls, "years": years,  "now_year": now_year}
        )

    else:

        calls = jsonable_encoder((call_memo[:]))
        model_calls = []
        res_model = info
        res_model['point2'] = rtf_to_text(res_model['point2'])

        res_model['point_str'] = res_model['point2'].split('\n')

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
                print(call)
                if not call['memo'] == None:
                    model_calls.append({'title': call['title'], 'memo': call['memo'].split('\r\n'), 'rcode': call['rcode']})
            model_calls = list(reversed(model_calls))

        except:
            print('통화메모 내림차순 에러발생')

        # 모델 전용 세부 페이지로 이동
        return templates.TemplateResponse(
            "page-user_model.html", {"request": req,
                                        'item': res_model,
                                        'activities': jsonable_encoder(activities[:]),
                                        "model_calls": model_calls, "years": years,  "now_year": now_year}
        )
        
    # except:
    #     print('에러 발생: ')
    #     pass



######################
# 영상 정보
@ router.get("/img_mov/{codesys}")
def mov_info(req: Request, codesys: str = '', db: Session = Depends(get_db)):


    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]

    print('영상 정보 페이지 접속..', codesys)
    res_mov = img_mov_info(db=db, codesys=codesys)

    res_mov = jsonable_encoder(res_mov[:])

    if not res_mov:
        
        return templates.TemplateResponse(
                "page-actmov.html", {"request": req, "text": '존재하지 않습니다.', "years": years,  "now_year": now_year}
    )
    else:
        

        mov_list = []
        for mov in res_mov:
            mov_list.append(mov)
            print(mov)

        return templates.TemplateResponse(
                    "page-actmov.html", {"request": req, "mov": mov_list, "years": years,  "now_year": now_year}
        )



@ router.get("/act_mov/{codesys}")
def mov_info(req: Request, codesys: str = '', db: Session = Depends(get_db)):

    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]

    print('영상 정보 페이지 접속..', codesys)
    res_mov = act_mov_info(db=db, codesys=codesys)

    res_mov = jsonable_encoder(res_mov[:])


    if not res_mov:
        
        return templates.TemplateResponse(
                "page-actmov.html", {"request": req, "text": '존재하지 않습니다.', "years": years,  "now_year": now_year}
    )
    else:
        

        mov_list = []
        for mov in res_mov:
            mov_list.append(mov)
            print(mov)

        return templates.TemplateResponse(
                    "page-actmov.html", {"request": req, "mov": mov_list, "years": years,  "now_year": now_year}
        )


@ router.get("/cf_mov/{codesys}")
def mov_info(req: Request, codesys: str = '', db: Session = Depends(get_db)):


    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]

    print('영상 정보 페이지 접속..', codesys)
    res_mov = cf_mov_info(db=db, codesys=codesys)

    res_mov = jsonable_encoder(res_mov[:])

    if not res_mov:
        
        return templates.TemplateResponse(
                "page-actmov.html", {"request": req, "text": '존재하지 않습니다.', "years": years,  "now_year": now_year}
    )
    else:
        

        mov_list = []
        for mov in res_mov:
            mov_list.append(mov)
            print(mov)

        return templates.TemplateResponse(
                    "page-actmov.html", {"request": req, "mov": mov_list, "years": years,  "now_year": now_year}
        )