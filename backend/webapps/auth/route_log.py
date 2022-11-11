from ast import Str
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


@router.post("/main")
def access_main(request: Request, db: Session = Depends(get_db)):

    user_id: str = request.cookies.get("usr")

    if user_id:

        now = datetime.now() + timedelta(hours=9)

        update_logs(user_id, request.client.host, request.__dict__['_headers']['user-agent'],
        now, 'main', db=db)



@router.post("/model_info/{code}")
def access_model_info(request: Request, code: str, db: Session = Depends(get_db)):

    user_id: str = request.cookies.get("usr")
    # print(request.__dict__)

    if user_id:

        now = datetime.now() + timedelta(hours=9)

        update_logs(user_id, request.client.host, request.__dict__['_headers']['user-agent'],
        now, 'model_info', db=db, action=code)