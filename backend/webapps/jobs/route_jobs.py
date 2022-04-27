from pyexpat import model
from time import time
from fastapi import APIRouter, Depends
from fastapi import Request, status, responses, Response
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.repository.jobs import list_jobs, search_job, list_models, chu_30
from db.repository.jobs import retrieve_job, create_new_job
from sqlalchemy import String, true
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.users import User
from apis.version1.route_login import get_current_user_from_token
from webapps.jobs.forms import JobCreateForm
from schemas.jobs import JobCreate
from typing import Optional
from fastapi.encoders import jsonable_encoder

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    jobs = list_jobs(db=db)
    return templates.TemplateResponse(
        "jobs/homepage.html", {"request": request, "jobs": jobs, "msg": msg}
    )


@router.get("/detail/{id}")
def job_detail(id: int, request: Request, db: Session = Depends(get_db)):
    job = retrieve_job(id=id, db=db)
    return templates.TemplateResponse(
        "jobs/detail.html", {"request": request, "job": job}
    )


@router.get("/post-a-job")
def create_job(request: Request):
    return templates.TemplateResponse("jobs/create_job.html", {"request": request})


@router.post("/post-a-job")
async def create_job(request: Request, db: Session = Depends(get_db)):
    form = JobCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(token)
            current_user: User = get_current_user_from_token(
                token=param, db=db)
            job = JobCreate(**form.__dict__)
            job = create_new_job(job=job, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/detail/{job.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in,In case problem persists, please contact us."
            )
            return templates.TemplateResponse("jobs/create_job.html", form.__dict__)
    return templates.TemplateResponse("jobs/create_job.html", form.__dict__)


@router.get("/update-delete-job")
def show_jobs_to_delete(request: Request, db: Session = Depends(get_db)):
    model_ = chu_30(db=db)
    chu_models = jsonable_encoder(model_[:])
    model_list = []
    mcodes = []
    i = 0
    print('데이터 개수: ', len(jsonable_encoder(model_[:])))

    for model in chu_models:

        if len(model_list) == 0:
            model_list.append({'mcode': model['Chu19']['mcode'], 'name': model['People']['name'],
                               'gubun': model['Chu19']['gubun'], 'jum': model['Chu19']['jum']})
            mcodes.append(model_list[i]['mcode'])

        elif model['Chu19']['mcode'] in mcodes:
            for i in range(len(model_list)):
                if model_list[i]['mcode'] == model['Chu19']['mcode']:
                    model_list[i]['jum'] += model['Chu19']['jum']

        else:
            model_list.append({'mcode': model['Chu19']['mcode'], 'name': model['People']['name'],
                               'gubun': model['Chu19']['gubun'], 'jum': model['Chu19']['jum']})
            mcodes.append(model_list[len(model_list) - 1]['mcode'])

        i += 1

    return templates.TemplateResponse(
        "jobs/show_jobs_to_update_delete.html", {
            "request": request, "jobs": model_list, "token": True}
    )


@ router.get("/chu2022/{date}")
def recommend_2022(request: Request, date: str, db: Session = Depends(get_db),):
    models = list_models(date=date, db=db)
    print('models입니다. ', jsonable_encoder(models[0:20]))

    return jsonable_encoder(models[:])
    # return templates.TemplateResponse(
    #     "jobs/show_jobs_to_update_delete.html", {
    #         "request": request, "jobss": jsonable_encoder(models[0:20]), "token": True}
    # )

# @router.get("/update-delete-job")
# def show_jobs_to_delete(request: Request, db: Session = Depends(get_db)):
#     jobs = list_jobs(db=db)
#     return templates.TemplateResponse(
#         "jobs/show_jobs_to_update_delete.html", {"request": request, "jobs": jobs}
#     )


# @ router.get("/aa/{data}")
# def recommend_2022(request: Request, data: str, db: Session = Depends(get_db),):
#     # models = list_models(date=date, db=db)
#     _date = JSON.stringify(data)
#     print('models입니다. ', _date)

    # return jsonable_encoder(models[:])


@ router.get("/updatejob/{id}")
def updatejob(id: int, request: Request, db: Session = Depends(get_db)):
    job = retrieve_job(id=id, db=db)
    print(job)
    print('데이터 개수: ', len(job))
    return templates.TemplateResponse(
        "jobs/update_job.html", {"request": request, "job": job}
    )


@ router.get("/search/")
def search(query: Optional[str], request: Request, db: Session = Depends(get_db)):
    jobs = search_job(query, db=db)
    print(jobs)
    print('데이터 개수: ', len(jobs))
    return templates.TemplateResponse(
        "jobs/homepage.html", {"request": request, "jobs": jobs}
    )
