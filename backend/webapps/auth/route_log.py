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
from core.hashing import Hasher
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta


router = APIRouter() 


@router.post("/main")
def access_main(request: Request, db: Session = Depends(get_db)):


    # 접속 id, ip, device, 날짜, 화면(main),
    
    req = request.__dict__['_headers']
    # id
    print(' route log :: ', req)

