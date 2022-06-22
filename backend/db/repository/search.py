from ast import Str
from asyncore import write
from curses import reset_prog_mode
from datetime import date, datetime, timedelta
import imp
import json
from mmap import mmap
from ntpath import join
from pickle import PERSID
from statistics import mode
from tkinter import HIDDEN
from xmlrpc.server import SimpleXMLRPCRequestHandler
from fastapi.encoders import jsonable_encoder
from numpy import sort
from sqlalchemy import between, desc, not_
from sqlalchemy.sql.expression import func

from sqlalchemy.orm import Session
from schemas.jobs import JobCreate
from db.models.kmodels import  People2
from db.models.kmodels import People, Chu19, Movsel, Mmeeting_proc, Yeon, SunokStar, SunokStarChu, SCount, Read, Mtel, Memo, Section, ModelCF, ModelMov
from db.models.yeons import RealTimeCF, RealTimeDRAMA
from dateutil.relativedelta import relativedelta
 

## 연령 분류(무식하게 짠 버전)
def divide_ages(models_info, search_ages):
    ## 나이 범위에 따라 구별

    print('연령 선택: ',search_ages)
    choi = models_info.filter( (People.age <= search_ages[0][0]) & (People.age >= search_ages[0][1]))
    
    return choi

    
## 알파모델료 분류(무식하게 짠 버전)
def divide_alpha(divide_age_models, hidden_alpha_fee):
    hidden_alpha_fee = hidden_alpha_fee.split(',')

    length = len(hidden_alpha_fee)

    # 레디자동 모델이 hidden_alpha_fee에 있으면 체크
    #
    print('알파모델료 선택11: ',hidden_alpha_fee)

    two_year = str(datetime.now().year - 2) + '.' + str(datetime.now().month) + '.' + str(datetime.now().day) 
    if length == 1:
        if 'ready' in hidden_alpha_fee:
            res_models = divide_age_models.filter((People.rdcode.contains('TKMA') | People.rdcode.contains('TKMB') | People.rdcode.contains('TKMV') | People.rdcode.contains('TKMF') | People.rdcode.contains('TKC')
            | People.rdcode.contains('TKHB') | People.rdcode.contains('TKHA') | People.rdcode.contains('TKHP') | People.rdcode.contains('TKHC') ) & ((People.mfee == hidden_alpha_fee[0]) | (People.mfee == '') & (People.rdate >= two_year) )) 
            
            res_models = jsonable_encoder(res_models[:])
            
            for model in res_models:
                if model['mfee'] == '':
                    model['mfee'] = '레디자동'
            print(res_models)
            return res_models

        else:
            res_models = divide_age_models.filter(People.mfee == hidden_alpha_fee[0])
            return res_models

        

    elif length == 2:
        if 'ready' in hidden_alpha_fee:
            print('aaa', hidden_alpha_fee)

            res_models = divide_age_models.filter((People.rdcode.contains('TKMA') | People.rdcode.contains('TKMB') | People.rdcode.contains('TKMV') | People.rdcode.contains('TKMF') | People.rdcode.contains('TKC')
            | People.rdcode.contains('TKHB') | People.rdcode.contains('TKHA') | People.rdcode.contains('TKHP') | People.rdcode.contains('TKHC') )
            & ((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) | (People.mfee == '') & (People.rdate >= two_year))) 
           

            res_models = jsonable_encoder(res_models[:])
            
            for model in res_models:
                if model['mfee'] == '':
                    model['mfee'] = '레디자동'
            print(res_models)
            return res_models

        else:
            res_models = divide_age_models.filter((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]))
            return res_models

    elif length == 3:
        
        if 'ready' in hidden_alpha_fee:
            print('aaa', hidden_alpha_fee)

            res_models = divide_age_models.filter((People.rdcode.contains('TKMA') | People.rdcode.contains('TKMB') | People.rdcode.contains('TKMV') | People.rdcode.contains('TKMF') | People.rdcode.contains('TKC')
            | People.rdcode.contains('TKHB') | People.rdcode.contains('TKHA') | People.rdcode.contains('TKHP') | People.rdcode.contains('TKHC') )
            & ((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) |(People.mfee == hidden_alpha_fee[2]) | (People.mfee == '') & (People.rdate >= two_year)) 
            )

            res_models = jsonable_encoder(res_models[:])
            
            for model in res_models:
                if model['mfee'] == '':
                    model['mfee'] = '레디자동'
            print(res_models)
            return res_models

        else:
            res_models = divide_age_models.filter((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) |
            (People.mfee == hidden_alpha_fee[2]) )
            return res_models


    elif length == 4:
        
        if 'ready' in hidden_alpha_fee:
            print('aaa', hidden_alpha_fee)

            res_models = divide_age_models.filter((People.rdcode.contains('TKMA') | People.rdcode.contains('TKMB') | People.rdcode.contains('TKMV') | People.rdcode.contains('TKMF') | People.rdcode.contains('TKC')
            | People.rdcode.contains('TKHB') | People.rdcode.contains('TKHA') | People.rdcode.contains('TKHP') | People.rdcode.contains('TKHC') )
            & ((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) | (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) | (People.mfee == '') & (People.rdate >= two_year)) 
            )

            res_models = jsonable_encoder(res_models[:])
            
            for model in res_models:
                if model['mfee'] == '':
                    model['mfee'] = '레디자동'
            print(res_models)
            return res_models

        else:
            res_models = divide_age_models.filter((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) |
            (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]))
            return res_models

    elif length == 5:
        
        if 'ready' in hidden_alpha_fee:
            print('aaa', hidden_alpha_fee)

            res_models = divide_age_models.filter((People.rdcode.contains('TKMA') | People.rdcode.contains('TKMB') | People.rdcode.contains('TKMV') | People.rdcode.contains('TKMF') | People.rdcode.contains('TKC')
            | People.rdcode.contains('TKHB') | People.rdcode.contains('TKHA') | People.rdcode.contains('TKHP') | People.rdcode.contains('TKHC') )
            & ((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) | (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) | (People.mfee == hidden_alpha_fee[4]) | ((People.mfee == '') & (People.rdate >= two_year))) 
            )

            res_models = jsonable_encoder(res_models[:])
            
            for model in res_models:
                if model['mfee'] == '':
                    model['mfee'] = '레디자동'
            print(res_models)
            return res_models

        else:
            res_models = divide_age_models.filter((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1])|
            (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) |
            (People.mfee == hidden_alpha_fee[4]))
            return res_models

    elif length == 6:
        
        if 'ready' in hidden_alpha_fee:
            print('aaa', hidden_alpha_fee)

            res_models = divide_age_models.filter((People.rdcode.contains('TKMA') | People.rdcode.contains('TKMB') | People.rdcode.contains('TKMV') | People.rdcode.contains('TKMF') | People.rdcode.contains('TKC')
            | People.rdcode.contains('TKHB') | People.rdcode.contains('TKHA') | People.rdcode.contains('TKHP') | People.rdcode.contains('TKHC') )
            & ((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) | (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) | (People.mfee == hidden_alpha_fee[4]) | (People.mfee == hidden_alpha_fee[5]) | ((People.mfee == '') & (People.rdate >= two_year))) 
            )

            res_models = jsonable_encoder(res_models[:])
            
            for model in res_models:
                if model['mfee'] == '':
                    model['mfee'] = '레디자동'
            print(res_models)
            return res_models

        else:

            res_models = divide_age_models.filter((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1])|
            (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) |
            (People.mfee == hidden_alpha_fee[4]) | (People.mfee == hidden_alpha_fee[5]))
            return res_models


    elif length == 7:
        
        if 'ready' in hidden_alpha_fee:
            print('aaa', hidden_alpha_fee)

            res_models = divide_age_models.filter((People.rdcode.contains('TKMA') | People.rdcode.contains('TKMB') | People.rdcode.contains('TKMV') | People.rdcode.contains('TKMF') | People.rdcode.contains('TKC')
            | People.rdcode.contains('TKHB') | People.rdcode.contains('TKHA') | People.rdcode.contains('TKHP') | People.rdcode.contains('TKHC') )
            & ((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) | (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) | (People.mfee == hidden_alpha_fee[4]) | (People.mfee == hidden_alpha_fee[5]) | (People.mfee == hidden_alpha_fee[6]) | ((People.mfee == '') & (People.rdate >= two_year))) 
            )

            res_models = jsonable_encoder(res_models[:])
            
            for model in res_models:
                if model['mfee'] == '':
                    model['mfee'] = '레디자동'
            print(res_models)
            return res_models

        else:

            res_models = divide_age_models.filter((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1])|
            (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) |
            (People.mfee == hidden_alpha_fee[4]) | (People.mfee == hidden_alpha_fee[5])|
            (People.mfee == hidden_alpha_fee[6]))
            return res_models
    
    
    elif length == 8:
    

        if 'ready' in hidden_alpha_fee:
            print('aaa', hidden_alpha_fee)

            res_models = divide_age_models.filter((People.rdcode.contains('TKMA') | People.rdcode.contains('TKMB') | People.rdcode.contains('TKMV') | People.rdcode.contains('TKMF') | People.rdcode.contains('TKC')
            | People.rdcode.contains('TKHB') | People.rdcode.contains('TKHA') | People.rdcode.contains('TKHP') | People.rdcode.contains('TKHC') )
            & ((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) | (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) | (People.mfee == hidden_alpha_fee[4]) | (People.mfee == hidden_alpha_fee[5]) | (People.mfee == hidden_alpha_fee[6])| (People.mfee == hidden_alpha_fee[7]) | ((People.mfee == '') & (People.rdate >= two_year))) 
            )

            res_models = jsonable_encoder(res_models[:])
            
            for model in res_models:
                if model['mfee'] == '':
                    model['mfee'] = '레디자동'
            print(res_models)
            return res_models

        else:

            res_models = divide_age_models.filter((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1])|
            (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) |
            (People.mfee == hidden_alpha_fee[4]) | (People.mfee == hidden_alpha_fee[5])|
            (People.mfee == hidden_alpha_fee[6]) | (People.mfee == hidden_alpha_fee[7]))
            return res_models
    
    elif length == 9:

        res_models = divide_age_models.filter((People.rdcode.contains('TKMA') | People.rdcode.contains('TKMB') | People.rdcode.contains('TKMV') | People.rdcode.contains('TKMF') | People.rdcode.contains('TKC')
        | People.rdcode.contains('TKHB') | People.rdcode.contains('TKHA') | People.rdcode.contains('TKHP') | People.rdcode.contains('TKHC') )
        & ((People.mfee == hidden_alpha_fee[0]) | (People.mfee == hidden_alpha_fee[1]) | (People.mfee == hidden_alpha_fee[2]) | (People.mfee == hidden_alpha_fee[3]) | (People.mfee == hidden_alpha_fee[4]) | (People.mfee == hidden_alpha_fee[5]) | (People.mfee == hidden_alpha_fee[6])| (People.mfee == hidden_alpha_fee[7])| (People.mfee == hidden_alpha_fee[8]) | ((People.mfee == '') & (People.rdate >= two_year))) 
        )

        res_models = jsonable_encoder(res_models[:])
        
        for model in res_models:
            if model['mfee'] == '':
                model['mfee'] = '레디자동'
        print(res_models)
        return res_models


# 셀럽 모델료 구분 (무식하게 짠 버전)
def divide_mfee(divide_age_models, hidden_celeb_fee, hidden_celeb_fee_month):

    print('안녕하세요, 셀럽 모델료 TEST: ', hidden_celeb_fee)

    length = len(hidden_celeb_fee)
    celeb_fee = hidden_celeb_fee.split(',')
    

    fee_dict = {'fee_all' : '', 'fee_100m': '1', 'fee_400m': '4', 'fee_400m_': '4.01', 'fee_no': 'X'}
    month_dict = {'three_month': 'a_3', 'six_month': 'a_6', 'one_year': 'a_12'}

    print(month_dict)

    if celeb_fee[0] == 'fee_100m':
        if 'fee_no' in celeb_fee: # length: 3 /// 날짜, 모델료 필터 
            if celeb_fee[2] == 'three_months':
                res_models = divide_age_models.filter((Yeon.a_3 <= 1) | (Yeon.a_3 == 0))
                return res_models

            elif celeb_fee[2] == 'six_months':
                res_models = divide_age_models.filter((Yeon.a_6 <= 1 ) | (Yeon.a_6 == 0))
                return res_models
            elif celeb_fee[2] == 'one_year':
                res_models = divide_age_models.filter((Yeon.a_12 <= 1) | (Yeon.a_12 == 0)) 
                return res_models  


        elif not 'fee_no' in celeb_fee: # length: 3 /// 날짜, 모델료 필터 
            if celeb_fee[1] == 'three_months':
                return divide_age_models.filter((Yeon.a_3 <= 1) & (Yeon.a_3 != 0))
            elif celeb_fee[1] == 'six_months':
                return divide_age_models.filter((Yeon.a_6 <= 1) & (Yeon.a_6 != 0))
            elif celeb_fee[1] == 'one_year':
                return divide_age_models.filter((Yeon.a_12 <= 1) & (Yeon.a_12 != 0)) 


    if celeb_fee[0] == 'fee_400m':
        if 'fee_no' in celeb_fee: # length: 3 /// 날짜, 모델료 필터 
            if celeb_fee[2] == 'three_months':
                return divide_age_models.filter(((Yeon.a_3 <= 4) & (Yeon.a_3 >= 1)) | (Yeon.a_3 == 0))
            elif celeb_fee[2] == 'six_months':
                return divide_age_models.filter(((Yeon.a_6 <= 4) & (Yeon.a_6 >= 1)) | (Yeon.a_6 == 0))
            elif celeb_fee[2] == 'one_year':
                return divide_age_models.filter(((Yeon.a_12 <= 4) & (Yeon.a_12 >= 1)) | (Yeon.a_12 == 0))   
        

        elif not 'fee_no' in celeb_fee: # length: 3 /// 날짜, 모델료 필터 
            if celeb_fee[1] == 'three_months':
                return divide_age_models.filter((Yeon.a_3 <= 4) & (Yeon.a_3 >= 1) & (Yeon.a_3 != 0))
            elif celeb_fee[1] == 'six_months':
                return divide_age_models.filter((Yeon.a_6 <= 4) & (Yeon.a_6 >= 1) & (Yeon.a_6 != 0)) 
            elif celeb_fee[1] == 'one_year':
                return divide_age_models.filter((Yeon.a_12 <= 4) & (Yeon.a_12 >= 1) & (Yeon.a_12 != 0) ) 



    if celeb_fee[0] == 'fee_400m_':
        if 'fee_no' in celeb_fee: # length: 3 /// 날짜, 모델료 필터 
            if celeb_fee[2] == 'three_months':
                return divide_age_models.filter((Yeon.a_3 >= 4) | (Yeon.a_3 == 0))
            elif celeb_fee[2] == 'six_months':
                return divide_age_models.filter((Yeon.a_6 >= 4) | (Yeon.a_6 == 0))
            elif celeb_fee[2] == 'one_year':
                return divide_age_models.filter((Yeon.a_12 >= 4) | (Yeon.a_12 == 0))   


        elif not 'fee_no' in celeb_fee: 
            if celeb_fee[1] == 'three_months':
                return divide_age_models.filter((Yeon.a_3 >= 4) & (Yeon.a_3 != 0))
            elif celeb_fee[1] == 'six_months':
                return divide_age_models.filter((Yeon.a_6 >= 4) & (Yeon.a_6 != 0))
            elif celeb_fee[1] == 'one_year':
                return divide_age_models.filter((Yeon.a_12 >= 4) & (Yeon.a_12 != 0)) 
    
    else:
        return divide_age_models
       
    # ['fee_400m_', 'fee_no', 'three_months']



def celeb_section(res_model, hidden_celeb_section):
    
    print('테스트 중입니다.', hidden_celeb_section)

    if len(hidden_celeb_section) == 0:
        hidden_celeb_section = 'section_all,section_singer,section_actor,section_idol,section_entertainment,section_broadcast,section_celeb,section_youtube'

    print(hidden_celeb_section, len(hidden_celeb_section))
    sections = hidden_celeb_section.split(',')
    section_code = []
    # 히든섹션 값이 model.json에 있으면 필터 함수 적용 시키고, 아니면 적용 시키지 않음]

    try:

        with open("model.json", 'r', encoding='utf-8') as json_file:
            aa = json.load(json_file)

            length = len(sections)
            print(sections)

            for section in sections:
                section_code.append(aa['model_section'][section])

            print('kkk: ', section_code)
            if length == 1:
                print(section_code)
                return res_model.filter(Yeon.rdcode.contains(section_code))
            elif length == 2:
                print(section_code)
                return res_model.filter(Yeon.rdcode.contains(section_code[0]) | Yeon.rdcode.contains(section_code[1]))
            elif length == 3:
                print(section_code)
                return res_model.filter(Yeon.rdcode.contains(section_code[0]) | Yeon.rdcode.contains(section_code[1]) | Yeon.rdcode.contains(section_code[2]))
            elif length == 4:
                print(section_code)
                return res_model.filter(Yeon.rdcode.contains(section_code[0]) | Yeon.rdcode.contains(section_code[1]) | Yeon.rdcode.contains(section_code[2])
                    | Yeon.rdcode.contains(section_code[3]))
            elif length == 5:
                print(section_code)
                return res_model.filter(Yeon.rdcode.contains(section_code[0]) | Yeon.rdcode.contains(section_code[1]) | Yeon.rdcode.contains(section_code[2])
                    | Yeon.rdcode.contains(section_code[3]) | Yeon.rdcode.contains(section_code[4]))
            elif length == 6:
                print(section_code)
                return res_model.filter(Yeon.rdcode.contains(section_code[0]) | Yeon.rdcode.contains(section_code[1])| Yeon.rdcode.contains(section_code[2])
                    | Yeon.rdcode.contains(section_code[3]) | Yeon.rdcode.contains(section_code[4]) | Yeon.rdcode.contains(section_code[5]))
            elif length == 8:
                return res_model
        
    except:
        print('일치하는 모델섹션이 json파일에 없음.')
        pass
   
    
def create_new_job(job: JobCreate, db: Session, owner_id: int):
    job = Job(**job.dict(), owner_id=owner_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def retrieve_job(id: int, db: Session):
    job = db.query(Job).filter(Job.id == id).first()
    return job


def list_jobs(db: Session):
    jobs = db.query(Job).filter(Job.is_active == True).all()
    return jobs


# 모델(추천2022)_기간검색
def list_models(date: str, db: Session):

    start_date = datetime.strptime(date[0:10], "%Y-%m-%d")
    end_date = datetime.strptime(date[11:20], "%Y-%m-%d")

    chu = db.query(Chu19, People).join(
        People, Chu19.mcode == People.codesys).where(start_date <= Chu19.edit_time)

    print(datetime.today())
    print(chu[0])
    return chu


# 추천2022_30일추천
def chu_30(db: Session, chu_img, chu_fav, chu_act, gender_w, gender_m, search_ages, hidden_alpha_fee, hidden_echar, hidden_rchar):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    char_list = []

    result_models = []
    char_list = hidden_echar.split(',') + hidden_rchar.split(',')

    
    chu = db.query((Chu19.mcode), Chu19.gubun, (Chu19.jum), People.mfee, People.name, People.sex, People.coname,  People.height, People.age, People.isyeon, People.image, Chu19.edit_time ).join(
        People, Chu19.mcode == People.codesys).filter((Chu19.edit_time >= (datetime.today() - relativedelta(months=1)))).filter((People.sex == gender_m) | (People.sex == gender_w))

    divide_age_models = divide_ages(models_info=chu, search_ages=search_ages)
    res_model = divide_alpha(divide_age_models=divide_age_models, hidden_alpha_fee=hidden_alpha_fee)
    
    res_model = jsonable_encoder(res_model[:])

    print(res_model)
    # for mm in res_model:
    #     print('vvvvvvvvvvv: ', mm)
    # print('캐릭터 선택 리스트: ', char_list)
    
    if  (char_list[0] == '') and  (char_list[1]== ''):
        return res_model
        
    else:
        for model in res_model:
            for char in char_list:
                if (char in model['image']):
                    if not char == '':
                        result_models.append(model)
        return result_models

    
    

# 추천2022_영상초이
def movchoi(db: Session, s_date, e_date,gender_w, gender_m, search_ages, hidden_alpha_fee, hidden_echar, hidden_rchar):

    e_date = datetime.strptime(e_date, "%Y-%m-%d")
    e_date = e_date + timedelta(days=1)
    # print(s_date, e_date)
    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    char_list = []

    result_models = []
    char_list = hidden_echar.split(',') + hidden_rchar.split(',')

    models_info = db.query((Movsel.mcode),  People.name, Movsel.rno, Movsel.edit_time, People.age, People.mfee, People.sex, People.coname,  People.height,  People.isyeon, People.image).join(
            People, Movsel.mcode == People.codesys).filter((People.sex == gender_m) | (People.sex == gender_w)).filter((Movsel.edit_time >= (datetime.today() - relativedelta(months=10))))

    divide_age_models = divide_ages(models_info=models_info,search_ages=search_ages)

    res_model = divide_alpha(divide_age_models=divide_age_models, hidden_alpha_fee=hidden_alpha_fee)

    res_model = jsonable_encoder(res_model[:])
    print('캐릭터 선택 리스트: ', char_list)
    
    if  (char_list[0] == '') and  (char_list[1]== ''):
        return res_model
            
    else:
        for model in res_model:
            for char in char_list:
                if (char in model['image']):
                    if not char == '':
                        result_models.append(model)
        return result_models
    


# 추천2022_프로카운트
def proc(db: Session, s_date, e_date, gender_w, gender_m, search_ages, hidden_alpha_fee, model, celeb, hidden_echar, hidden_rchar):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    char_list = []
    print(gender_w, gender_m)

    result_models = []
    char_list = hidden_echar.split(',') + hidden_rchar.split(',')

    # if (celeb) and (not model):
    #     proc = db.query(Mmeeting_proc.mcode, People.name, People.sex, People.age, People.coname,  People.height, Mmeeting_proc.edit_time, Mmeeting_proc.projcode, People.isyeon,  People.image).join(
    #         People, Mmeeting_proc.mcode == People.codesys).filter((Mmeeting_proc.edit_time >= s_date) & (Mmeeting_proc.edit_time <= e_date)).filter((People.sex == gender_m) | (People.sex == gender_w)).filter(
    #             People.rdcode.contains('TC')

    #     )
    #     divide_age_models = divide_ages(models_info=proc, search_ages=search_ages)
    #     res_model = divide_alpha(divide_age_models=divide_age_models, hidden_alpha_fee=hidden_alpha_fee)
    #     gubun = 'celeb'
    if (model) and (not celeb):

        proc = db.query(Mmeeting_proc.mcode, People.name, People.sex, People.age, People.coname, People.mfee, People.height, Mmeeting_proc.edit_time, Mmeeting_proc.projcode, People.isyeon, People.image).join(
            People, Mmeeting_proc.mcode == People.codesys).filter((Mmeeting_proc.edit_time >= s_date) & (Mmeeting_proc.edit_time <= e_date)).filter((People.sex == gender_m) | (People.sex == gender_w)).filter(
                not_(People.rdcode.contains('TC'))
        )
        divide_age_models = divide_ages(models_info=proc, search_ages=search_ages)
        
        res_model = divide_alpha(divide_age_models=divide_age_models, hidden_alpha_fee=hidden_alpha_fee)

        gubun = 'model'

        res_model = jsonable_encoder(res_model[:])
        print('캐릭터 선택 리스트: ', char_list)
        
        if  (char_list[0] == '') and  (char_list[1]== ''):
            return res_model, gubun
            
        else:
            for model in res_model:
                for char in char_list:
                    if (char in model['image']):
                        if not char == '':
                            result_models.append(model)
            return result_models, gubun

    # else:
    #     print('ddddddd: ', s_date, e_date)

    #     proc = db.query(Mmeeting_proc.mcode, People.name, Mmeeting_proc.edit_time, Mmeeting_proc.projcode, People.isyeon,  People.image).join(
    #         People, Mmeeting_proc.mcode == People.codesys).filter((Mmeeting_proc.edit_time >= s_date) & (Mmeeting_proc.edit_time <= e_date)).filter((People.sex == gender_m) | (People.sex == gender_w))
    #     divide_age_models = divide_ages(models_info=proc, search_ages=search_ages)
    #     res_model = divide_alpha(divide_age_models=divide_age_models, hidden_alpha_fee=hidden_alpha_fee)
        
    #     gubun = 'all'

    # else:
    #     proc = db.query(Mmeeting_proc.mcode.label('codesys'), Yeon.rno, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, Mmeeting_proc.edit_time, Mmeeting_proc.projcode, People.isyeon,  People.image).join(
    #         Yeon, Mmeeting_proc.mcode == Yeon.codesys).join(People, People.codesys == Yeon.codesys).filter((Mmeeting_proc.edit_time >= s_date) & (Mmeeting_proc.edit_time <= e_date)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(
    #             Yeon.rdcode.contains('TC'))

    #     gubun = 'celeb'

    # for model in jsonable_encoder(res_model[:]):
    #     print(model['mfee'], model['age'])


        


# 순옥스타_최신등록순
def order_register(db: Session, gender_w, gender_m, search_ages , hidden_celeb_fee, hidden_celeb_fee_month, hidden_celeb_section):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    print('haha...: ', hidden_celeb_section)
    register = db.query(SunokStar.mcode, Yeon.name, SunokStar.edit_time,  Yeon.sex.label('gender'), Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, People.isyeon, People.height, People.coname, People.mfee).join(
        Yeon, SunokStar.mcode == Yeon.codesys).join(
        People, SunokStar.mcode == People.codesys).order_by(desc(SunokStar.edit_time)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w))

    
    divide_age_models = divide_ages(register, search_ages)
    
    res_model = divide_mfee(divide_age_models, hidden_celeb_fee, hidden_celeb_fee_month)
    
    res_celeb = celeb_section(res_model, hidden_celeb_section)
    print(res_celeb)
    return res_celeb


# 순옥스타_추천순
def order_recommend(db: Session, gender_w, gender_m, search_ages, hidden_celeb_fee, hidden_celeb_fee_month , hidden_celeb_section):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    register = db.query(SunokStarChu.edit_time, SunokStarChu.frcode, SunokStar.rcode, SunokStar.mcode, SunokStarChu.jum1, SunokStarChu.jum2, Yeon.sex, Yeon.name, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, People.isyeon, People.height, People.coname, People.mfee).order_by(desc(SunokStar.edit_time)).join(People, People.codesys == SunokStar.mcode).filter(
        SunokStar.rcode == SunokStarChu.frcode).filter(SunokStar.mcode == Yeon.codesys).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w))
    
    divide_age_models = divide_ages(register, search_ages)
    res_model = divide_mfee(divide_age_models, hidden_celeb_fee, hidden_celeb_fee_month)

    res_celeb = celeb_section(res_model, hidden_celeb_section)
    return res_celeb





# 순옥스타_s카운트순
def order_s_count(db: Session, gender_w, gender_m, search_ages, hidden_celeb_fee, hidden_celeb_fee_month , hidden_celeb_section, s_date, e_date):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    # print('안녕하세요용: ', search_ages)
    models = db.query(SCount.edit_time, SCount.mcode, Yeon.sex, Yeon.name, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, People.isyeon, People.height, People.coname, People.mfee).join(
        Yeon, SCount.mcode == Yeon.codesys).join(People, SCount.mcode == People.codesys).join(SunokStar, SunokStar.mcode == SCount.mcode).order_by(desc(SCount.edit_time)).filter((SCount.edit_time >= s_date) & (
            SCount.edit_time <= e_date)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w))

    divide_age_models = divide_ages(models, search_ages)
    res_model = divide_mfee(divide_age_models, hidden_celeb_fee, hidden_celeb_fee_month)

    res_celeb = celeb_section(res_model, hidden_celeb_section)
    return res_celeb


# 셀럽검색_열람횟수
def order_read(db: Session, gender_w, gender_m, search_ages, s_date, e_date, hidden_celeb_fee, hidden_celeb_fee_month, hidden_celeb_section):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

   
    # 3개월 모델료 기준.
    models = db.query(Read.edit_time, Read.mcode, Yeon.sex, Yeon.name, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, People.isyeon, People.height, People.coname, People.mfee).join(
        Yeon, Read.mcode == Yeon.codesys).join(People, Read.mcode == People.codesys).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(People.isyeon == 'V').filter((Read.edit_time >= (datetime.today() - relativedelta(months=3))))

    divide_age_models = divide_ages(models, search_ages)
    res_model = divide_mfee(divide_age_models, hidden_celeb_fee, hidden_celeb_fee_month)

    res_celeb = celeb_section(res_model, hidden_celeb_section)
    return res_celeb


# 셀럽검색_실베스타
def order_realtime(db: Session, gender_w, gender_m, search_ages, hidden_celeb_fee, hidden_celeb_fee_month , hidden_celeb_section):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    year = str(datetime.today().year)
    month = str(datetime.today().month)
    day = str(datetime.today().day)

    if len(month) == 1:
        month = '0' + str(datetime.today().month)
    if len(day) == 1:
        day = '0' + str(datetime.today().day)

    # 3개월 모델료 기준.
    print((year) + '.' + month + '.' + day)
    # 셀럽 계약현황
    real_time_cf = db.query(Yeon.codesys, Yeon.rno, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, RealTimeCF.brand, RealTimeCF.dend.label('cf_dend'), People.isyeon, People.isyeon, People.height, People.coname, People.mfee).join(
        RealTimeCF, Yeon.codesys == RealTimeCF.codesys).join(People, People.codesys == Yeon.codesys).filter(
            (RealTimeCF.dend >= (year) + '.' + month + '.' + day)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w))

    # 활동내역
    real_time_activity = db.query(Yeon.codesys, Yeon.rno, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, RealTimeDRAMA.title, RealTimeDRAMA.dend.label('drama_dend'), People.isyeon, People.isyeon, People.height, People.coname, People.mfee).join(
        RealTimeDRAMA, Yeon.codesys == RealTimeDRAMA.codesys).join(People, People.codesys == Yeon.codesys).filter(
            (RealTimeDRAMA.dend >= (year) + '.' + month + '.' + day)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w))

    divide_age_cf = divide_ages(real_time_cf, search_ages)
    divide_age_activity = divide_ages(real_time_activity, search_ages)

    res_model_cf = divide_mfee(divide_age_cf, hidden_celeb_fee, hidden_celeb_fee_month)
    res_model_activity = divide_mfee(divide_age_activity, hidden_celeb_fee, hidden_celeb_fee_month)

    res_celeb_cf = celeb_section(res_model_cf, hidden_celeb_section)
    res_celeb_activity = celeb_section(res_model_activity, hidden_celeb_section)
    # 셀럽 프로카운트는 mmeeting_proc 에서
    return res_celeb_cf, res_celeb_activity



def proc_celeb(db: Session, gender_w, gender_m, search_ages, hidden_celeb_fee, hidden_celeb_fee_month , hidden_celeb_section, s_date, e_date):
    
    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    proc = db.query(Mmeeting_proc.mcode.label('codesys'), Yeon.rno, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, Mmeeting_proc.edit_time, Mmeeting_proc.projcode, People.isyeon, People.isyeon, People.height, People.coname, People.mfee).join(
            Yeon, Mmeeting_proc.mcode == Yeon.codesys).join(People, People.codesys == Yeon.codesys).filter(Mmeeting_proc.edit_time >= (datetime.today() - relativedelta(months=3))).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(
                Yeon.rdcode.contains('TC'))

    divide_age_models = divide_ages(proc, search_ages)
    res_models = divide_mfee(divide_age_models, hidden_celeb_fee,hidden_celeb_fee_month)

    res_celeb = celeb_section(res_models, hidden_celeb_section)

    return res_celeb



def search_job(db: Session, name='', coname='', tel='', manager=''):

    two_year = str(datetime.now().year - 2) + '.' + str(datetime.now().month) + '.' + str(datetime.now().day)

    models = db.query(People.codesys.label('mcode'), People.name, People.age, People.sex.label('gender'), People.coname, People.mfee, People.rdate, People.rdcode,
                      People.height, People.sex, People.isyeon).filter(People.name.contains(name) & People.coname.contains(coname) & (People.dam.contains(manager) | People.dam2.contains(manager) | People.dam3.contains(manager)) &
                                                                       (People.tel1.contains(tel) | People.dam2tel.contains(tel) | People.dam3tel.contains(tel) | People.ptel.contains(tel)))
# 
    models = jsonable_encoder(models[:])
    for model in models:
        if (model['rdate'] >= two_year) and (model['mfee'] == '') and (('TKMA' in model['rdcode']) or ('TKMB' in model['rdcode']) or ('TKMV' in model['rdcode']) or ('TKMF' in model['rdcode']) or ('TKC' in model['rdcode']) or ('TKHA' in model['rdcode']) or ('TKHB' in model['rdcode']) or ('TKHC' in model['rdcode']) or ('TKHP' in model['rdcode'])):
            model['mfee'] = '레디자동'
        
    return models


def search_celeb(db: Session, mcode):
    # celeb = db.query(Yeon.codesys, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12,).filter(Yeon.name.contains(query))


    models = db.query(People.codesys.label('mcode'), People.name, People.age, People.sex.label('gender'), People.coname, People.mfee,
                      People.height, People.sex, Yeon.a_3, Yeon.a_6, Yeon.a_12, People.isyeon).join(Yeon, Yeon.codesys == People.codesys).filter(People.codesys == mcode)

    

    return models


def models_info(db: Session, codesys):

    # 세부정보
    # rno를 api서버로 가져감. rno에 해당되는 Yeon.codesys를 조회함.
    # 여기 없으면 People.codesys의 no으로 인식하고, rno와 일치하는 no에 해당하는People.codesys를 조회함.
    # Yeon에서 가져온 경우에는 연예인 세부정보를 뿌려주고, (모델료, 모델 정보[이름, 나이, 키, 성별, 소속사, 연락처, 인스타, 포인트, 메일], 계약현황, 레디진행 이력, 활동 내역, 통화 메모)
    # People에서 가져온 경우에는 모델 세부정보를 뿌려준다. (알파 모델료, 모델정보[이름, 나이, 키, 성별, 소속사, 연락처, 인스타, 포인트, 메일], 신체 사이즈, 통화 메모), 경력 사항 확인 필요


    try:

        # 셀럽, 모델 통화메모
        call_memo = db.query(People.codesys, People.name, People.age, People.height, People.sex, People.coname, People.dam, People.tel1,
                             People.dam2, People.dam2tel, People.dam3, People.dam3tel, People.sns2, People.insta_flw_str, Memo.title, Memo.rcode, Memo.memo).join(
            Memo, Memo.code == People.codesys).filter(codesys == People.codesys)
        # 셀럽 세부정보
        yeon_detail = db.query(Yeon.codesys, Yeon.rno, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, Yeon.height, People.coname, People.dam, People.tel1,
                               People.dam2, People.dam2tel, People.dam3, People.dam3tel, People.sns2, People.insta_flw_str,  People.rdcode, Mtel.point2,
                               RealTimeCF.brand, RealTimeCF.poom, RealTimeCF.imonth, RealTimeCF.fee, RealTimeCF.dstart, RealTimeCF.dend, RealTimeCF.indefin, RealTimeCF.nation, RealTimeCF.writer, RealTimeCF.wrdate, People2.mail1
                               ).join(Yeon, Yeon.codesys == People.codesys).join(Mtel, Mtel.mcode == People.codesys).join(
            RealTimeCF, People.codesys == RealTimeCF.codesys).join(People2, People.codesys == People2.codesys).filter(codesys == Yeon.codesys)

        yeon_activity = db.query(Yeon.codesys, Yeon.rno, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, Yeon.height,
                                 RealTimeDRAMA.drgubun, RealTimeDRAMA.drgubun2, RealTimeDRAMA.title, RealTimeDRAMA.dstart, RealTimeDRAMA.dend, RealTimeDRAMA.writer, RealTimeDRAMA.wrdate).join(
            Yeon, Yeon.codesys == RealTimeDRAMA.codesys).filter(codesys == Yeon.codesys)

        # 일반모델 세부정보
        model_detail = db.query(People.codesys, People.name, People.age, People.height, People.sex, People.coname, People.dam, People.tel1, People.rdcode, People.mfee, People.bun,
                                People.dam2, People.dam2tel, People.dam3, People.dam3tel, People.sns2, People.insta_flw_str, People.ptel, Mtel.point2, People2.bodysize, People2.mail1).join(
            Mtel, Mtel.mcode == People.codesys).join(People2, People.codesys == People2.codesys).filter(codesys == People.codesys)

        # 모델 섹션
        model_section = db.query(
            Section.no, Section.edit_time, Section.code, Section.title)

        # 모델_에스더 광고이력
        model_cf = db.query(ModelCF.brand, ModelCF.poom, ModelCF.imonth, ModelCF.fee, ModelCF.dstart, ModelCF.dend, ModelCF.rdjin, ModelCF.indefin, ModelCF.nation, ModelCF.writer, ModelCF.wrdate).filter(
            codesys == ModelCF.codesys)

        if jsonable_encoder(yeon_detail[:]):

            model = jsonable_encoder(model_detail[0])
            section = jsonable_encoder(model_section[:])
            model_section = model['rdcode'].split('/')
            title = []
            aa = []

            for i in range(len(section)):
                if section[i]['code'] in model_section:
                    title.append(section[i]['title'])

            model['rdcode'] = "/".join(title)

            return yeon_detail, yeon_activity, call_memo, 321

        else:
            print('일반 k 모델입니다.')
            model = jsonable_encoder(model_detail[0])
            section = jsonable_encoder(model_section[:])
            model_section = model['rdcode'].split('/')
            title = []
            aa = []

            for i in range(len(section)):
                if section[i]['code'] in model_section:
                    title.append(section[i]['title'])

            model['rdcode'] = "/".join(title)
            return model, model_cf, call_memo, 123
    except:
        return 123

## 이미지영상
def img_mov_info(db: Session, codesys):
    
    try:
        return db.query(ModelMov.edit_time, ModelMov.mcode, ModelMov.fname, ModelMov.fext, ModelMov.fpath).filter(ModelMov.mcode == codesys).filter(ModelMov.fpath.contains('AA영상')).filter(ModelMov.fext.contains('mp4'))

    except:
        pass

## 연기영상
def act_mov_info(db: Session, codesys):
    
    try:
        return db.query(ModelMov.edit_time, ModelMov.mcode, ModelMov.fname, ModelMov.fext, ModelMov.fpath).filter(ModelMov.mcode == codesys).filter(ModelMov.fpath.contains('AA연기')).filter(ModelMov.fext.contains('mp4'))

    except:
        pass

## 연기영상
def cf_mov_info(db: Session, codesys):
    
    try:
        return db.query(ModelMov.edit_time, ModelMov.mcode, ModelMov.fname, ModelMov.fext, ModelMov.fpath).filter(ModelMov.mcode == codesys).filter(ModelMov.fpath.contains('AA광고')).filter(ModelMov.fext.contains('mp4'))

    except:
        pass

