from datetime import date, datetime, timedelta
import json
from math import dist
from fastapi.encoders import jsonable_encoder
from sqlalchemy import between, desc, distinct, not_ 
from sqlalchemy.sql import func

from sqlalchemy.orm import Session

from db.models.kmodels import People, Recommendation_month, Movsel, Movsel_box, Procount
from db.projects.project import ProjectContract

from dateutil.relativedelta import relativedelta
 

# 공통 필터 항목들 : 성별, 연령, 알파모델료
def common_filter(db, gender: list, age: list, mfee:list):
    
    # 나이 범위 변수
    this_year = datetime.now().year
    min_age_year = this_year - int(age[0]) + 1
    max_age_year = this_year - int(age[1]) + 1

    # 성별 값 변경
    if 'm' in gender:
        gender[gender.index('m')] = '남'
    if 'w' in gender:
        gender[gender.index('w')] = '여'
    if '' in gender:
        gender.pop(gender.index(''))


    # 알파모델료에 해당하는 DB key값 추출 변수
    key_alpha_fee = []
    
    with open("model.json", 'r', encoding='utf-8') as json_file:
        dict_model_fee = json.load(json_file)
        list_model_fee = [x.split('~') for x in dict_model_fee['model_fee'].values()]

    for i in range(len(list_model_fee)):
        try:
            if ((int(mfee[0]) >= int(list_model_fee[i][0]) and int(mfee[0]) <= int(list_model_fee[i][1])) or 
            (int(mfee[1]) >= int(list_model_fee[i][0]) and ((int(mfee[1]) <= int(list_model_fee[i][1]))))
            or (list_model_fee[i][1] == '0')
            ):
                
                key_alpha_fee.append(i)
            
        except:
            
            continue
    # 알파모델료에 해당하는 DB key값 추출

    if len(key_alpha_fee) == 2:
        key_alpha_fee = list(dict_model_fee['model_fee'].keys())[key_alpha_fee[0]: key_alpha_fee[1]+1]
    else:
        
        key_alpha_fee.append(list(dict_model_fee['model_fee'].keys())[key_alpha_fee[0]])
        key_alpha_fee.pop(0)
    # 상훈페이는 체크박스 -> 선택 되었으면 별도로 리스트에 추가
    if '0100' in mfee:
        key_alpha_fee.append('0100')

    

    print('알파모델료 :: ', key_alpha_fee)
    print('나이 구간 :: ', max_age_year, min_age_year)
    print('성별 :: ', gender)
    # 연령 필터링
    models = db.filter((People.age >= max_age_year) & (People.age <= min_age_year))
    # 성별 필터링
    models = models.filter(People.sex.in_(gender))
    #알파모델료 필터링
    models = models.filter(People.mfee.in_(key_alpha_fee))


    return models


# 30일추천 모델 리스트
def search_recommendation_month(db: Session, gender: list, age: list, mfee: list, recommendation_section: list):


    # print(recommendation_section)
    models = db.query(Recommendation_month.mcode, Recommendation_month.gubun, func.sum(Recommendation_month.jum).label('sum_jum') , Recommendation_month.edit_time, People.mfee, People.name, People.sex, People.coname,  People.height, People.age, People.isyeon, People.image
    ).join(
        People, Recommendation_month.mcode == People.codesys
    ).filter(
        (Recommendation_month.gubun.in_(recommendation_section)) & (Recommendation_month.edit_time >= (datetime.today() - relativedelta(months=1))) & (not_(Recommendation_month.jum == 0))).group_by(People.codesys).order_by(desc(func.sum(Recommendation_month.jum))
    )

    models = common_filter(models, gender, age, mfee)

    
    res_model = jsonable_encoder(models[:])


    return res_model


# 영상초이 모델 리스트
def search_mov_choi(db: Session, gender: list, age: list, mfee:list):

    models = db.query(Movsel.mcode, People.name, People.mfee, People.name, People.sex, People.coname,  People.height, People.age, People.isyeon, func.count(distinct(Movsel.worksss)).label('choi_count'), Movsel_box.edit_time, Movsel_box.projname
        ).join(
            Movsel_box, Movsel.frcode == Movsel_box.rcode
        ).join(
            People, People.codesys == Movsel.mcode
        ).filter(
            Movsel_box.edit_time >= (datetime.today() - relativedelta(months=12))
        ).group_by(
            Movsel.mcode
        ).order_by(
            desc(func.count(distinct(Movsel.worksss)))
        )

    models = common_filter(models, gender, age, mfee)
    models = models.limit(500)
    

    return jsonable_encoder(models[:])



# 프로카운트 모델 리스트
def search_procount(db:Session, gender: list, age: list, mfee: list):
    
    models = db.query(Procount.title, Procount.idate, Procount.mcode, People.name, People.mfee, People.name, People.sex, People.coname,  People.height, People.age, People.isyeon, func.count(distinct(Procount.projcode)).label('project_count')
    ).join(
        People, People.codesys == Procount.mcode
    ).filter(
        (Procount.idate >= str((datetime.today() - relativedelta(months=12)).date()).replace('-', '.')) & (not_(People.isyeon == 'V'))
    ).group_by(
        Procount.mcode
    ).order_by(
        desc(func.count(Procount.projcode))
    )


    print('프로카운트 :: ', str((datetime.today() - relativedelta(months=12)).date()))

    models = common_filter(models, gender, age, mfee)

    return jsonable_encoder(models[:])