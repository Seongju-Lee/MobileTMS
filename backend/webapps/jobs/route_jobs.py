from pyexpat import model
from time import time
import turtle
from fastapi import APIRouter, Depends
from fastapi import Request, status, responses, Response, requests
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.repository.jobs import list_jobs, search_job, list_models, chu_30
from db.repository.jobs import retrieve_job, create_new_job
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


# @router.get("/")
# def home(request: Request, db: Session = Depends(get_db), msg: str = None):
#     jobs = list_jobs(db=db)
#     return templates.TemplateResponse(
#         "jobs/homepage.html", {"request": request, "jobs": jobs, "msg": msg}
#     )
@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    # model_ = chu_30(db=db, s_date='1', e_date='2')
    # chu_models = jsonable_encoder(model_[:])
    # model_list = []
    # mcodes = []
    # i = 0
    # print('데이터 개수: ', len(jsonable_encoder(model_[:])))

    # for model in chu_models:

    #     if len(model_list) == 0:
    #         model_list.append({'mcode': model['Chu19']['mcode'], 'name': model['People']['name'],
    #                            'gubun': model['Chu19']['gubun'], 'jum': model['Chu19']['jum']})
    #         mcodes.append(model_list[i]['mcode'])

    #     elif model['Chu19']['mcode'] in mcodes:
    #         for i in range(len(model_list)):
    #             if model_list[i]['mcode'] == model['Chu19']['mcode']:
    #                 model_list[i]['jum'] += model['Chu19']['jum']

    #     else:
    #         model_list.append({'mcode': model['Chu19']['mcode'], 'name': model['People']['name'],
    #                            'gubun': model['Chu19']['gubun'], 'jum': model['Chu19']['jum']})
    #         mcodes.append(model_list[len(model_list) - 1]['mcode'])

    #     i += 1

    # print(model_list)

    return templates.TemplateResponse(
        "jobs/homepage.html", {"request": request}
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
    model_ = chu_30(db=db, s_date='1', e_date='2')
    chu_models = jsonable_encoder(model_[:])
    model_list = []
    mcodes = []
    i = 0
    print('데이터 개수: ', (jsonable_encoder(model_[:])))

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

    print(model_list)
    return templates.TemplateResponse(
        "jobs/show_jobs_to_update_delete.html", {
            "request": request, "jobs": model_list, "token": True}
    )


# 필터내용
@ router.get("/filter")
def search_filter(req: Request, s_date: str = '', e_date: str = '', gender_m: str = '', gender_w: str = '',
                  age1: str = '', age2: str = '', age3: str = '', age4: str = '', age5: str = '',
                  s_img: str = '', e_img: str = '', s_fav: str = '', e_fav: str = '', s_act: str = '', e_act: str = '', sort_thrdays: str = '', sort_movchoi: str = '', sort_proc: str = '',
                  db: Session = Depends(get_db)):

    # 추천 30일
    if sort_thrdays:
        if s_img or s_fav or s_act:
            models = chu_30(db=db, chu_act=s_act,
                            chu_fav=s_fav, chu_img=s_img)

            img_ok, fav_ok, act_ok = False, False, False
            chu_models = jsonable_encoder(models[:])
            res_models = []
            i = 0
            df = pd.DataFrame(chu_models).groupby(
                ['mcode', 'gubun', 'name']).sum().reset_index()

            print(df[:])
            print(df.shape)

            # {'mcode': '93B20F4BB002', 'gubun': 'act', 'name': '양보람', 'jum': 9}
            search_models = df.values.tolist()
            filter_models = []
            output_models = []
            for model in (search_models):

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
                    # print(i)
                    if res_models[i]['mcode'] == res_models[i-1]['mcode']:

                        res_models[i].update(res_models[i-1])
                    else:
                        filter_models.append(res_models[i-1])

                    i += 1

            for model in filter_models:
                if ('img_jum' in model.keys()) and (model['img_jum'] >= int(s_img) and model['img_jum'] <= int(e_img)):
                    img_ok = True
                if ('fav_jum' in model.keys()) and (model['fav_jum'] >= int(s_img) and model['fav_jum'] <= int(e_img)):
                    fav_ok = True
                if ('act_jum' in model.keys()) and (model['act_jum'] >= int(s_img) and model['act_jum'] <= int(e_img)):
                    act_ok = True
                print('ouuuuutt: ', model)
                if img_ok and fav_ok and act_ok:

                    output_models.append(model)
                img_ok, fav_ok, act_ok = False, False, False

            # if model[1] == 'img' and (model[3] >= int(s_img) and (model[3]) <= int(e_img)):
            #     output_models
            # if model[1] == 'fav' and (model[3] >= int(s_fav) and (model[3]) <= int(e_fav)):
            # print('ouuuuutt: ', output_models)
            return templates.TemplateResponse(
                "jobs/homepage.html", {"request": req,
                                       "jobs": jsonable_encoder(filter_models[:100])}
            )


@ router.get("/chu2022")
def recommend_2022(request: Request, date: str, db: Session = Depends(get_db)):

    models = list_models(date=date, db=db)
    print('models입니다. ', jsonable_encoder(models[0:20]))
    print('123: ', request)
    return jsonable_encoder(models[:])


@ router.get("/search")
def search(query: Optional[str], request: Request, db: Session = Depends(get_db)):
    jobs = search_job(query, db=db)

    return templates.TemplateResponse(
        "jobs/homepage.html", {"request": request, "jobs": jobs}
    )
