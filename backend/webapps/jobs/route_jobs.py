from pyexpat import model
from time import time
from fastapi import APIRouter, Depends
from fastapi import Request, status, responses, Response, requests
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.repository.jobs import list_jobs, search_job, list_models, chu_30
from db.repository.jobs import retrieve_job, create_new_job
from sqlalchemy import String, null, true
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

    print(model_list)
    return templates.TemplateResponse(
        "jobs/show_jobs_to_update_delete.html", {
            "request": request, "jobs": model_list, "token": True}
    )


# 필터내용
@ router.get("/filter")
def search_filter(req: Request, s_date: str = '', e_date: str = '', gender_m: str = '', gender_w: str = '',
                  age1: str = '', age2: str = '', age3: str = '', age4: str = '', age5: str = '',
                  chu_img: str = '', chu_fav: str = '', chu_act: str = '', sort_thrdays: str = '', sort_movchoi: str = '', sort_proc: str = '',
                  db: Session = Depends(get_db)):

    # 추천 30일
    if sort_thrdays:
        if chu_img or chu_fav or chu_act:
            models = chu_30(db=db, chu_act=chu_act,
                            chu_fav=chu_fav, chu_img=chu_img)

            print(chu_img, chu_fav, chu_act)

            chu_models = jsonable_encoder(models[:])
            # print('aaaa', chu_models)
            img_mcode = []
            fav_mcode = []
            act_mcode = []

            # 모델 추천 항목별 리스트 생성.
            img_list = []
            fav_list = []
            act_list = []
            for model in chu_models:

                # 호감도 선택
                if model['Chu19']['gubun'] == 'fav':

                    if model['Chu19']['mcode'] in fav_mcode:

                        for i in range(len(fav_list)):

                            if fav_list[i]['mcode'] == model['Chu19']['mcode']:
                                fav_list[i]['jum'] += model['Chu19']['jum']

                    else:
                        fav_list.append(
                            {'mcode': model['Chu19']['mcode'], 'jum': model['Chu19']['jum'], 'name': model['People']['name'], 'sex': model['People']['sex'], 'age': model['People']['age'], 'height': model['People']['height']})

                        fav_mcode.append(model['Chu19']['mcode'])

                # 이미지 선택
                elif model['Chu19']['gubun'] == 'img':

                    if model['Chu19']['mcode'] in img_mcode:

                        for i in range(len(img_list)):

                            if img_list[i]['mcode'] == model['Chu19']['mcode']:
                                img_list[i]['jum'] += model['Chu19']['jum']

                    else:
                        img_list.append(
                            {'mcode': model['Chu19']['mcode'], 'jum': model['Chu19']['jum'], 'name': model['People']['name'], 'sex': model['People']['sex'], 'age': model['People']['age'], 'height': model['People']['height']})

                        img_mcode.append(model['Chu19']['mcode'])

                # 연기력 선택
                elif model['Chu19']['gubun'] == 'act':

                    if model['Chu19']['mcode'] in act_mcode:

                        for i in range(len(act_list)):

                            if act_list[i]['mcode'] == model['Chu19']['mcode']:
                                act_list[i]['jum'] += model['Chu19']['jum']

                    else:
                        act_list.append(
                            {'mcode': model['Chu19']['mcode'], 'jum': model['Chu19']['jum'], 'name': model['People']['name'], 'sex': model['People']['sex'], 'age': model['People']['age'], 'height': model['People']['height']})

                        act_mcode.append(model['Chu19']['mcode'])

            print('fav: ', fav_list)
            print('act: ', act_list)
            print(img_list[1])

            a = [chu_img, chu_fav, chu_act]
            if not '' in a:  # 모두 다 선택
                print('ALL')

                models = set(set(fav_mcode) | set(act_mcode) | set(img_mcode))
                print(models)  # set해서 mcode다 뽑음. 비교하면 됨.

            else:
                pos = [i for i in range(len(a)) if a[i] == '']
                print('선택 항목: ', pos)

            return templates.TemplateResponse(
                "jobs/homepage.html", {"request": req,
                                       "jobs": jsonable_encoder(fav_list[:20])}
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
    # print(jobs)
    # print('데이터 개수: ', len(jobs))
    return templates.TemplateResponse(
        "jobs/homepage.html", {"request": request, "jobs": jobs}
    )
