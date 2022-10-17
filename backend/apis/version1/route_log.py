from ast import Str
from turtle import update
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import APIRouter, Request
from db.session import get_db
from sqlalchemy.orm import Session
from core.config import settings
from datetime import timedelta
from core.security import create_access_token
from db.repository.login import get_users
from db.repository.logs import update_logs
from core.hashing import Hasher
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta


router = APIRouter() 



def update_model_info_log(request: Request, code: str, isCeleb , db: Session = Depends(get_db)):
    user_id: str = request.cookies.get("usr")

    print("POST /celeb/" + code)
    print("user ID: " + user_id)

    if user_id:

        if request.url.hostname == '127.0.0.1' or request.url.hostname == 'localhost':
            now = datetime.now()
        else:
            now = datetime.now() + timedelta(hours=9)

        if isCeleb:
            update_logs(user_id, request.client.host, request.__dict__['_headers']['user-agent'],
            now, 'celeb-info', db=db, action=code)
        else:
            update_logs(user_id, request.client.host, request.__dict__['_headers']['user-agent'],
            now, 'model-info', db=db, action=code)


def update_project_info_log(request: Request, code: str , db: Session = Depends(get_db)):
    user_id: str = request.cookies.get("usr")

    print("POST /celeb/" + code)
    print("user ID: " + user_id)

    if user_id:

        if request.url.hostname == '127.0.0.1' or request.url.hostname == 'localhost':
            now = datetime.now()
        else:
            now = datetime.now() + timedelta(hours=9)

        
        update_logs(user_id, request.client.host, request.__dict__['_headers']['user-agent'],
        now, 'project-info', db=db, action=code)
        


@router.post("/main")
def access_main(request: Request, db: Session = Depends(get_db)):

    user_id: str = request.cookies.get("usr")

    if user_id:

        now = datetime.now() + timedelta(hours=9)

        update_logs(user_id, request.client.host, request.__dict__['_headers']['user-agent'],
        now, 'main', db=db)



# 셀럽 상세정보 열람
@router.post("/celebs/{code}")
def access_celeb_info(request: Request, code: str, db: Session = Depends(get_db)):

    update_model_info_log(request, code, True, db)
    


# k모델 상세정보 열람
@router.post("/models/{code}")
def access_celeb_info(request: Request, code: str, db: Session = Depends(get_db)):

    update_model_info_log(request, code, False, db)




# 셀럽 상세정보 열람
@router.post("/projects/{code}")
def access_celeb_info(request: Request, code: str, db: Session = Depends(get_db)):

    print('프로젝트 열람 코드 :: ', code)

    update_project_info_log(request, code, db)

    