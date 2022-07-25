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


        req = request.__dict__['_headers']
        
        ## id : usr
        print('USER ID :: ', user_id)

        ## ip : request.client.host
        print('USER IP :: ', request.client.host)

        ## device : user-agent
        print('USER DEVICE :: ' , request.__dict__['_headers']['user-agent'])
        ## 날짜 : datetime
        now = datetime.now() + timedelta(hours=9)
        print(now)

        ## 화면 : main
        print('USER SCREEN :: ' , 'main')

        update_logs(user_id, request.client.host, request.__dict__['_headers']['user-agent'],
        now, 'main', db=db)

    
