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






    #  token이 없을 때는 로그 넘기지 X      


    # token이 있을 때 - user_id 넘김.
    # 접속 id, ip, device, 날짜, 화면(main),
    
    req = request.__dict__['_headers']
    


    ## id : usr
    user_id: str = request.cookies.get("usr")
    print('USER ID :: ', user_id)

    ## ip : request.client.host
    print('USER IP :: ', request.client.host)

    ## device : user-agent
    print('USER DEVICE :: ' , request.__dict__['_headers']['user-agent'])
    ## 날짜 : datetime
    now = datetime.now()
    print(now)
    ## 화면 : main
    print('USER SCREEN :: ' , 'main')

    return req
    
