from datetime import date, datetime, timedelta
from functools import reduce
import json
from math import dist
from fastapi.encoders import jsonable_encoder
from numpy import product
from sqlalchemy import between, desc, distinct, not_, true 
from sqlalchemy.sql import func

from sqlalchemy.orm import Session

from db.models.kmodels import People, Recommendation_month, Movsel, Movsel_box, Procount, Yeon, ReadModel
from db.models.yeons import YeonCF, ContractDrama, SunokStar, ScountId, SunokStarRecommend
from db.models.users import Rusers

from dateutil.relativedelta import relativedelta
import pandas as pd

def common_filter_(db, gender: list, age: list, isYeon: bool):


    
    # 나이 범위 변수
    this_year = datetime.now().year
    min_age_year = str(this_year - int(age[0]) + 1)
    max_age_year = str(this_year - int(age[1]) + 1)

    # 성별 값 변경
    if 'm' in gender:
        gender[gender.index('m')] = '남'
    if 'w' in gender:
        gender[gender.index('w')] = '여'
    if '' in gender:
        gender.pop(gender.index(''))


    print('>=age : ', max_age_year)
    print('<=age : ', min_age_year)
    print('gender : ', gender)

    if isYeon:
        # 연령 필터링
        models = db.filter( ((Yeon.age >= max_age_year) & (Yeon.age <= min_age_year)) | (not_(Yeon.age)) )
        # 성별 필터링
        models = models.filter(Yeon.sex.in_(gender))
    else:
        # 연령 필터링
        models = db.filter( ((Yeon.age >= max_age_year) & (Yeon.age <= min_age_year)) | not_(Yeon.age))
        # 성별 필터링
        models = models.filter(People.sex.in_(gender))

    return models

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


    print('mfee ::: ', mfee)
    for i in range(len(list_model_fee)):
        try:
            # print('iiii -- :: ' ,  list_model_fee[i][0], list_model_fee[i][1])
            if '1550' in mfee:
                mfee[mfee.index('1550')] = '1500'
            if ((int(mfee[0]) >= int(list_model_fee[i][0]) and int(mfee[0]) <= int(list_model_fee[i][1])) or 
            (int(mfee[1]) >= int(list_model_fee[i][0]) and ((int(mfee[1]) <= int(list_model_fee[i][1]))))
            or (list_model_fee[i][1] == '0' and int(mfee[1]) >= 4100 )
            ):
                # print('iiii ++  :: ' , list_model_fee[i][0] ,list_model_fee[i][1])
                
                key_alpha_fee.append(i)
            
        except:
            continue

    print('key_alpha_fee ;::: ', key_alpha_fee)
    # 알파모델료에 해당하는 DB key값 추출
    # 범위지정
    if len(key_alpha_fee) == 2:
        key_alpha_fee = list(dict_model_fee['model_fee'].keys())[key_alpha_fee[0]: key_alpha_fee[1]+1]
    # 하나의 값 지정
    else:
        # print('key_alpha_fee-- :: ', key_alpha_fee)
        key_alpha_fee.append(list(dict_model_fee['model_fee'].keys())[key_alpha_fee[0]])
        key_alpha_fee.pop(0)

    # 상훈페이는 체크박스 -> 선택 되었으면 별도로 리스트에 추가
    if '0100' in mfee:
        key_alpha_fee.append('0100')

    # print('key_alpha_fee++ :: ', key_alpha_fee)
    # 연령 필터링
    models = db.filter(((People.age >= max_age_year) & (People.age <= min_age_year)))
    # 성별 필터링
    models = models.filter(People.sex.in_(gender))
    #알파모델료 필터링
    models = models.filter(People.mfee.in_(key_alpha_fee))


    return models



def celeb_filter(db, gender: list, age: list, cfee: list, section: list, period: str):

    # 나이, 연령 필터
    models = common_filter_(db, gender, age, True)

    # print('CFEE: ', cfee)
    print('SECTION: ', section)
    print('PERIOD: ', period)


    cfee = list(map(lambda x: float(x) if not x == '' else 0, cfee))
    

    print('CFEE: ', cfee)
    # 셀럽 모델료 필터
    if period == 'a_3':
        models = models.filter(((Yeon.a_3 >= cfee[0]) & (Yeon.a_3 <= cfee[1])))
        

    elif period == 'a_6':
        models = models.filter((Yeon.a_6 >= cfee[0]) & (Yeon.a_6 <= cfee[1]))
    else:
        models = models.filter((Yeon.a_12 >= cfee[0]) & (Yeon.a_12 <= cfee[1]))

    # 셀럽 섹션 필터
    with open("model.json", 'r', encoding='utf-8') as json_file:
        dict_model_section = json.load(json_file)['model_section']
        celeb_section = [dict_model_section['section_'+x] for x in section]
        celeb_section = reduce(lambda x,y : x+'|'+y , celeb_section)

    models = models.filter(Yeon.rdcode.regexp_match(celeb_section))

    return models


# 30일추천 모델 리스트
def search_recommendation_month(db: Session, gender: list, age: list, mfee: list, recommendation_section: list):


    print(recommendation_section)
    print(str((datetime.today() - relativedelta(months=1)).date()))

    models = db.query(Recommendation_month.mcode, Recommendation_month.gubun, func.sum(Recommendation_month.jum).label('sum_jum') , Recommendation_month.edit_time, People.mfee, People.name, People.sex, People.coname,  People.height, People.age, People.isyeon, People.image
    ).join(
        People, Recommendation_month.mcode == People.codesys
    ).join(
        Rusers, Rusers.uid == Recommendation_month.sawon
    ).filter(
        (Recommendation_month.gubun.in_(recommendation_section)) & (Recommendation_month.edit_time >= str((datetime.today() - relativedelta(months=1)).date())) & (not_(Recommendation_month.jum == 0)) & (not_(Rusers.power8.contains('/GTX/') & (func.length(Rusers.power8)< 20)))
    ).group_by(
        People.codesys
    ).order_by(
        desc(func.sum(Recommendation_month.jum))
    )

    print(models)
    for m in jsonable_encoder(models[:])[:20]:
        print(m)

    models = common_filter(models, gender, age, mfee)
    res_model = jsonable_encoder(models[:])

    # for m in res_model[:20]:
    #     print(m)


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
    
    models = db.query(Procount.title, Procount.idate, Procount.mcode, People.name, People.mfee, People.sex, People.coname,  People.height, People.age, People.isyeon, func.count(distinct(Procount.projcode)).label('project_count')
    ).join(
        People, People.codesys == Procount.mcode
    ).filter(
        (Procount.idate >= str((datetime.today() - relativedelta(months=12)).date()).replace('-', '.')) & (not_(People.isyeon == 'V'))
    ).group_by(
        Procount.mcode
    ).order_by(
        desc(func.count(Procount.projcode))
    )


    models = common_filter(models, gender, age, mfee)

    return jsonable_encoder(models[:])





### 셀럽 STRART #######

# 실베스타
def search_real_time(db: Session, gender: list, age: list, cfee: list, section: list, period: str):


    # 계약현황
    contracts_cf = db.query(People.codesys,Yeon.name, Yeon.a_3, Yeon.a_6, Yeon.a_12, Yeon.sex, People.coname,  Yeon.height, Yeon.age, func.count(People.codesys).label('contractCF')
            ).join(
                YeonCF, People.codesys == YeonCF.codesys
            ).join(
                Yeon, Yeon.codesys == People.codesys
            ).filter(
                YeonCF.dend >= str((datetime.today()).date()).replace('-', '.')
            ).group_by(
                YeonCF.codesys
            ).order_by(
                desc(func.count(YeonCF.codesys))
            )

    # TMS 데이터 자체가 올바르지 못함 --> 확인 필요.
    # 활동내역

    # contracts_drama = db.query(ContractDrama.title, ContractDrama.codesys, People.name, People.mfee, People.sex, People.coname,  People.height, People.age, People.isyeon, func.count(People.codesys).label('contractDrama')
    #         ).join(
    #             ContractDrama, People.codesys == ContractDrama.codesys
    #         ).filter(
    #             ContractDrama.dend >= str((datetime.today()).date()).replace('-', '.')
    #         ).group_by(
    #             ContractDrama.codesys
    #         ).order_by(
    #             desc(func.count(ContractDrama.codesys))
    #         )

    # 프로카운트
    procount = db.query(People.codesys, Yeon.name, Yeon.a_3, Yeon.a_6, Yeon.a_12, Yeon.sex, People.coname,  Yeon.height, Yeon.age,  func.count(distinct(Procount.projcode)).label('project_count')
    ).join(
        People, People.codesys == Procount.mcode
    ).join(
        Yeon, Yeon.codesys == People.codesys
    ).filter(
        (Procount.idate >= str((datetime.today() - relativedelta(months=3)).date()).replace('-', '.')) & ((People.isyeon == 'V'))
    ).group_by(
        Procount.mcode
    ).order_by(
        desc(func.count(Procount.projcode))
    )

    
    procount = celeb_filter(procount, gender, age, cfee, section, period)
    contracts_cf = celeb_filter(contracts_cf, gender, age, cfee, section, period)
    

    contracts_cf = jsonable_encoder(contracts_cf[:])
    procount = jsonable_encoder(procount[:])

  
    df_cf = pd.DataFrame(contracts_cf)
    df_project = pd.DataFrame(procount)

  
    df_merge = df_cf.merge(df_project, left_on=['codesys', 'name', 'sex', 'coname', 'height', 'age', 'a_3', 'a_6', 'a_12'], right_on=['codesys', 'name', 'sex', 'coname', 'height', 'age', 'a_3', 'a_6', 'a_12'], how='outer')
    df_merge = df_merge.fillna(0)

    # print(df_merge)
    models = df_merge[['codesys', 'name', 'sex', 'coname', 'height', 'age', 'a_3', 'a_6', 'a_12','contractCF', 'project_count']].to_dict(orient='records')
    models = sorted(models, key=lambda x : (x['contractCF']*3 + x['project_count']*3), reverse=True)

    
    
    return models[:100]
    
    # print(procount)

    # models = db.query(RealTime)


# 열람횟수 
def search_open_count(db: Session, gender: list, age: list, cfee: list, section: list, period: str):
    
    models = db.query(People.codesys, ReadModel.mcode, Yeon.name, Yeon.a_3, Yeon.a_6, Yeon.a_12, Yeon.sex, People.coname,  Yeon.height, Yeon.age, func.count(distinct(ReadModel.mcode)).label('read_count')
                ).join(
                    Yeon, ReadModel.mcode == Yeon.codesys
                ).join(
                    People, ReadModel.mcode == People.codesys
                ).filter(
                    (ReadModel.edit_time >= (datetime.today() - relativedelta(months=2))) &
                    (People.isyeon == 'V')
                ).group_by(
                    ReadModel.mcode
                ).order_by(
                    desc(func.count(ReadModel.mcode))
                )
         


    models = celeb_filter(models, gender, age, cfee, section, period)
    models = jsonable_encoder(models[:])

   
   
    return models





# 순옥스타_scount
def search_scount(db: Session, gender: list, age: list, cfee: list, section: list, period: str):
    
    models = db.query(SunokStar.mcode, SunokStar.mcode2, SunokStar.mcode3, SunokStar.mcode4 , SunokStar.suntitle, SunokStar.mea, func.count(ScountId.mcode) , ScountId.frcode, People.codesys,Yeon.name, Yeon.a_3, Yeon.a_6, Yeon.a_12, Yeon.sex, People.coname,  Yeon.height, Yeon.age
                ).join(
                    SunokStar, SunokStar.mcode == ScountId.mcode
                ).join(
                    People, ScountId.mcode == People.codesys
                ).join(
                    Yeon, People.codesys == Yeon.codesys
                ).filter(
                    ScountId.rdate >= str((datetime.today() - relativedelta(months=2)).date()).replace('-', '.') 
                ).group_by(
                    ScountId.mcode, SunokStar.mcode2
                ).order_by(
                    desc(func.count(ScountId.mcode))
                )
         

    models = celeb_filter(models, gender, age, cfee, section, period)
    models = jsonable_encoder(models[:])

   
   
    return models


# 순옥스타 추천순
def search_recommend(db: Session, gender: list, age: list, cfee: list, section: list, period: str):

    models = db.query(SunokStarRecommend.frcode, func.sum(SunokStarRecommend.jum1), func.sum(SunokStarRecommend.jum2), People.codesys,Yeon.name, Yeon.a_3, Yeon.a_6, Yeon.a_12, Yeon.sex, People.coname,  Yeon.height, Yeon.age
                ).join(
                    SunokStar, SunokStar.rcode == SunokStarRecommend.frcode
                ).join(
                    Yeon, Yeon.codesys == SunokStar.mcode
                ).join(
                    People, Yeon.codesys == People.codesys
                ).group_by(
                    SunokStarRecommend.frcode
                ).order_by(
                    desc(func.sum(SunokStarRecommend.jum1))
                )

    models = celeb_filter(models, gender, age, cfee, section, period)
    models = jsonable_encoder(models[:])

    return models

    