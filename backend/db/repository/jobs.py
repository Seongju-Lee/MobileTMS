from datetime import datetime, timedelta
import imp
from mmap import mmap
from fastapi.encoders import jsonable_encoder
from sqlalchemy import between, desc, not_
from sqlalchemy.sql.expression import func

from sqlalchemy.orm import Session
from schemas.jobs import JobCreate
from db.models.jobs import Job
from db.models.jobs import People, Chu19, Movsel, Mmeeting_proc, Yeon, SunokStar, SunokStarChu
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
def proc(db: Session, s_date, e_date, gender_w, gender_m, s_age, e_age, model, celeb):

    if gender_m:
        gender_m = '남'
    if gender_w:
        gender_w = '여'

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


def search_job(query: str, db: Session):
    jobs = db.query(Job).filter(Job.title.contains(query))
    return jobs
