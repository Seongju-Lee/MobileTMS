from datetime import datetime
import imp
from fastapi.encoders import jsonable_encoder
from sqlalchemy import between, desc, func
from sqlalchemy.orm import Session
from schemas.jobs import JobCreate
from db.models.jobs import Job
from db.models.jobs import People, Chu19
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
def chu_30(db: Session, chu_img, chu_fav, chu_act):

    print(']]]]]]]]]]]]]]]]] ', chu_img, chu_fav, chu_act)
    chu = db.query((Chu19.mcode), Chu19.gubun, func.sum(Chu19.jum), People.name).join(
        People, Chu19.mcode == People.codesys).group_by(Chu19.mcode, Chu19.gubun).order_by(Chu19.edit_time).where(((Chu19.gubun == chu_fav) | (Chu19.gubun == chu_img) | (Chu19.gubun == chu_act)) & (Chu19.edit_time >= (datetime.today() - relativedelta(months=1))))

    print('qqqq: ', chu)
    return chu


def update_job_by_id(id: int, job: JobCreate, db: Session, owner_id: int):
    existing_job = db.query(Job).filter(Job.id == id)
    if not existing_job.first():
        return 0

    # job.__dict__.update(owner_id=owner_id)
    try:
        existing_job.update(job.__dict__)
        db.commit()
    except Exception as e:
        print(e)
        return 1


def delete_job_by_id(id: int, db: Session, owner_id: int):
    existing_job = db.query(Job).filter(Job.id == id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1


def search_job(query: str, db: Session):
    jobs = db.query(Job).filter(Job.title.contains(query))
    return jobs
