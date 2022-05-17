from ast import Str
from asyncore import write
from datetime import datetime, timedelta
import imp
from mmap import mmap
from ntpath import join
from fastapi.encoders import jsonable_encoder
from numpy import sort
from sqlalchemy import between, desc, not_
from sqlalchemy.sql.expression import func

from sqlalchemy.orm import Session
from schemas.jobs import JobCreate
from db.models.jobs import Job, People2
from db.models.jobs import People, Chu19, Movsel, Mmeeting_proc, Yeon, SunokStar, SunokStarChu, SCount, Read, Mtel, Memo, Section, ModelCF
from db.models.yeons import RealTimeCF, RealTimeDRAMA
from dateutil.relativedelta import relativedelta


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
def chu_30(db: Session, chu_img, chu_fav, chu_act, gender_w, gender_m, s_age, e_age):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'
    print(gender_w, gender_m)
    print((e_age), (s_age))

    chu = db.query((Chu19.mcode), Chu19.gubun, People.name, (Chu19.jum)).join(
        People, Chu19.mcode == People.codesys).filter((Chu19.edit_time >= (datetime.today() - relativedelta(months=1)))).filter((People.sex == gender_m) | (People.sex == gender_w)).filter(People.age >= e_age)

    return chu


# 추천2022_영상초이
def movchoi(db: Session, s_date, e_date):

    e_date = datetime.strptime(e_date, "%Y-%m-%d")
    e_date = e_date + timedelta(days=1)
    print(s_date, e_date)
    choi = db.query((Movsel.mcode),  People.name, Movsel.rno, Movsel.edit_time).join(
        People, Movsel.mcode == People.codesys).where((Movsel.edit_time >= s_date) & (Movsel.edit_time <= e_date))

    return choi


# 추천2022_프로카운트
def proc(db: Session, s_date, e_date, gender_w, gender_m, s_age, e_age, model, celeb, sort_realtime):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    if not sort_realtime:
        if (celeb) and (not model):
            proc = db.query(Mmeeting_proc.mcode, People.name, Mmeeting_proc.edit_time, Mmeeting_proc.projcode).join(
                People, Mmeeting_proc.mcode == People.codesys).filter((Mmeeting_proc.edit_time >= s_date) & (Mmeeting_proc.edit_time <= e_date)).filter((People.sex == gender_m) | (People.sex == gender_w)).filter(People.age >= e_age).filter(
                    People.rdcode.contains('TC')
            )
        elif (model) and (not celeb):
            proc = db.query(Mmeeting_proc.mcode, People.name, Mmeeting_proc.edit_time, Mmeeting_proc.projcode).join(
                People, Mmeeting_proc.mcode == People.codesys).filter((Mmeeting_proc.edit_time >= s_date) & (Mmeeting_proc.edit_time <= e_date)).filter((People.sex == gender_m) | (People.sex == gender_w)).filter(People.age >= e_age).filter(
                    not_(People.rdcode.contains('TC'))
            )
        else:
            proc = db.query(Mmeeting_proc.mcode, People.name, Mmeeting_proc.edit_time, Mmeeting_proc.projcode).join(
                People, Mmeeting_proc.mcode == People.codesys).filter((Mmeeting_proc.edit_time >= s_date) & (Mmeeting_proc.edit_time <= e_date)).filter((People.sex == gender_m) | (People.sex == gender_w)).filter(People.age >= e_age)

    else:
        proc = db.query(Mmeeting_proc.mcode.label('codesys'), Yeon.rno, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, Mmeeting_proc.edit_time, Mmeeting_proc.projcode).join(
            Yeon, Mmeeting_proc.mcode == Yeon.codesys).filter((Mmeeting_proc.edit_time >= s_date) & (Mmeeting_proc.edit_time <= e_date)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(Yeon.age >= e_age).filter(
                Yeon.rdcode.contains('TC'))

    return proc


# 순옥스타_최신등록순
def order_register(db: Session, s_date, e_date, gender_w, gender_m, s_age, e_age, model, celeb):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

        register = db.query(SunokStar.mcode, Yeon.name, SunokStar.edit_time,  Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12).join(
            Yeon, SunokStar.mcode == Yeon.codesys).order_by(desc(SunokStar.edit_time)).filter((SunokStar.edit_time >= s_date) & (SunokStar.edit_time <= e_date)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(Yeon.age >= e_age)
    return register


# 순옥스타_추천순
def order_recommend(db: Session, gender_w, gender_m, s_age, e_age,):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    register = db.query(SunokStarChu.edit_time, SunokStarChu.frcode, SunokStar.rcode, SunokStar.mcode, SunokStarChu.jum1, SunokStarChu.jum2, Yeon.sex, Yeon.name, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12).order_by(desc(SunokStar.edit_time)).filter(
        SunokStar.rcode == SunokStarChu.frcode).filter(SunokStar.mcode == Yeon.codesys).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(Yeon.age >= e_age)
    return register


# 순옥스타_추천순
def order_s_count(db: Session, gender_w, gender_m, s_age, e_age, s_date, e_date):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    models = db.query(SCount.edit_time, SCount.mcode, Yeon.sex, Yeon.name, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12).join(
        Yeon, SCount.mcode == Yeon.codesys).order_by(desc(SCount.edit_time)).filter((SCount.edit_time >= s_date) & (
            SCount.edit_time <= e_date)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(Yeon.age >= e_age)

    return models


# 셀럽검색_열람횟수
def order_read(db: Session, gender_w, gender_m, s_age, e_age, s_date, e_date, s_fee, e_fee):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

    if s_fee == 0:
        s_fee = 'x'
    if e_fee == 0:
        e_fee = 'x'
    # 3개월 모델료 기준.
    models = db.query(Read.edit_time, Read.mcode, Yeon.sex, Yeon.name, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12).join(
        Yeon, Read.mcode == Yeon.codesys).order_by(desc(Read.edit_time)).filter((Read.edit_time >= s_date) & (
            Read.edit_time <= e_date)).filter((Yeon.a_3 >= s_fee) & (Yeon.a_3 <= e_fee)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(Yeon.age >= e_age)
    return models


# 셀럽검색_실베스타
def order_realtime(db: Session, gender_w, gender_m, s_age, e_age, s_fee, e_fee):

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
    real_time_cf = db.query(Yeon.codesys, Yeon.rno, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, RealTimeCF.brand, RealTimeCF.dend.label('cf_dend')).join(
        RealTimeCF, Yeon.codesys == RealTimeCF.codesys).filter(
            (RealTimeCF.dend >= (year) + '.' + month + '.' + day)).filter((Yeon.a_3 >= s_fee) & (Yeon.a_3 <= e_fee)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(Yeon.age >= e_age)

    # 활동내역
    real_time_activity = db.query(Yeon.codesys, Yeon.rno, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12, RealTimeDRAMA.title, RealTimeDRAMA.dend.label('drama_dend')).join(
        RealTimeDRAMA, Yeon.codesys == RealTimeDRAMA.codesys).filter(
            (RealTimeDRAMA.dend >= (year) + '.' + month + '.' + day)).filter((Yeon.a_3 >= s_fee) & (Yeon.a_3 <= e_fee)).filter((Yeon.sex == gender_m) | (Yeon.sex == gender_w)).filter(Yeon.age >= e_age)

    # 셀럽 프로카운트는 mmeeting_proc 에서
    return real_time_cf, real_time_activity


def search_job(query: str, db: Session):
    # celeb = db.query(Yeon.codesys, Yeon.name, Yeon.sex, Yeon.age, Yeon.a_3, Yeon.a_6, Yeon.a_12,).filter(Yeon.name.contains(query))

    models = db.query(People.codesys.label('mcode'), People.name, People.age,
                      People.height, People.sex).filter(People.name.contains(query))
    return models


def models_info(db: Session, codesys):

    # 세부정보
    # rno를 api서버로 가져감. rno에 해당되는 Yeon.codesys를 조회함.
    # 여기 없으면 People.codesys의 no으로 인식하고, rno와 일치하는 no에 해당하는People.codesys를 조회함.
    # Yeon에서 가져온 경우에는 연예인 세부정보를 뿌려주고, (모델료, 모델 정보[이름, 나이, 키, 성별, 소속사, 연락처, 인스타, 포인트, 메일], 계약현황, 레디진행 이력, 활동 내역, 통화 메모)
    # People에서 가져온 경우에는 모델 세부정보를 뿌려준다. (알파 모델료, 모델정보[이름, 나이, 키, 성별, 소속사, 연락처, 인스타, 포인트, 메일], 신체 사이즈, 통화 메모), 경력 사항 확인 필요

    # yeoncf.brand, yeoncf.poom , yeoncf.imonth, yeoncf.fee , yeoncf.dstart , yeoncf.dend , yeoncf.indefin , yeoncf.nation, yeoncf.writer , yeoncf.wrdate

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
