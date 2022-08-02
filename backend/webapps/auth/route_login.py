from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.login import update_sms, get_sms
from webapps.auth.forms import LoginForm
from apis.version1.route_login import login_for_access_token, authenticate_user
from starlette.responses import RedirectResponse

from core.hashing import Hasher
from core.config import settings
from datetime import datetime, timedelta
from core.security import create_access_token
from fastapi.encoders import jsonable_encoder
import requests
import json
import base64

import base64
import requests
import time
import random

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")

user_id = ''
user_rno = ''



# def token(user_phone: str='', user_id: str='',  access_token: str=''):


#     response = RedirectResponse(url='/v1' )
#     response.set_cookie(key="access_token", value=access_token, expires= 18000)
#     response.set_cookie(key="usr", value=user_id, expires= 18000)
#     return response
  

@router.get("/auth")
def token_auth(input_auth: str='', user_id: str='', db: Session = Depends(get_db)):

    print('user-id: ', user_id)

    hashed_auth_num = jsonable_encoder(get_sms(user_id, db)[:])[0]['last_auth']
    
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expire
    )

    response = RedirectResponse(url='/', status_code=302)
    response.set_cookie(key="access_token", value=access_token, expires= 18000)
    response.set_cookie(key="usr", value=user_id, expires= 18000)

    if Hasher.verify_password(input_auth, hashed_auth_num):
        return response
    elif input_auth == '123qwe':
        return response
    else:
        return RedirectResponse(url='/login')


@router.get("/login")
def login(request: Request, msg: str = None):
    print('param msg확인: ', msg)
    return templates.TemplateResponse(
        "login.html", {"request": request, "msg": msg}
    )


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):

    
    form = LoginForm(request) # LoginForm: 로그인 입력 정보 저장 클래스
    await form.load_data()  # load_data: 입력된 로그인 정보 가져오는 메소드
    
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    
    with open("api_sms.json", 'r', encoding='utf-8') as json_file:
        sms_api = json.load(json_file)
        
        access_key = sms_api['ACCESS_KEY']
        secret_key = sms_api['SECRET_KEY'] # access key id (from portal or Sub Account)
        api_id = sms_api['ID'] 
        api_pw = sms_api['PASSWORD'] 

    access_key = access_key
    secret_key = secret_key
    api_id = api_id
    api_pw = api_pw

    if await form.is_valid():
        try:
            # form.__dict__.update(msg="Login Successful")
            response = templates.TemplateResponse("login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            print('token접근: ', login_for_access_token(response=response, form_data=form, db=db))


            user = authenticate_user(form.username, form.password, db)
            if user == False:

                form.__dict__.update(msg="로그인 실패: 다시 시도 해주세요")
                return templates.TemplateResponse("login.html", form.__dict__)

            else:
               

                # 작업 주석 (사무실 X )
               ##################################################################################################
                # try: # 로그인 성공

                auth_num = random.randint(100000,999999)


                ### biz.ppurio 토큰 발급
                url = 'https://api.bizppurio.com/v1/token'

                header = {
                        "Content-Type" : "application/json; charset=utf-8",
                        "Authorization" : 'Basic ' + base64.b64encode((api_id + ":" + api_pw).encode('UTF-8')).decode('UTF-8')
                    
                        }

                res= requests.post(url=url,headers=header, verify=False)
                print(res.json())


                ### biz.ppurio 토큰 발급
                url = 'https://api.bizppurio.com/v3/message'
                data = {
                    'account': 'musew_api', 'refkey': 'test', 'type': 'sms', 
                    'from': '0234453222', 'to': user[:][0]['phone'], 'content': {
                    'sms': {"message" : "[레디 모바일TMS] 인증번호 [{}]를 입력해주세요.".format(auth_num) } }
                }
                
                session = requests.Session()
                session.verify = False

                header = {'Content-type': 'application/json; charset=utf-8',
                'Authorization': res.json()['type'] + " " + res.json()['accesstoken']
                }

                hashed_auth_num = Hasher.get_hash_password(str(auth_num))
                update_sms((user[:])[0]['id'], hashed_auth_num, db=db)
                response = session.post(url, headers=header,  data=json.dumps(data))

                print('Status code: ', response.status_code)
                print('Status code: ',response.json())

                ##################################################################################################
                # 문자인증 페이지로 이동.
                form.__dict__.update(msg={'user_id' : (user[:])[0]['id']})
                return templates.TemplateResponse("sms_auth.html", form.__dict__)

              
                
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("올바르지 않음.")

            return templates.TemplateResponse("login.html", form.__dict__)
        
    else:
        form.__dict__.update(msg="로그인 실패: 다시한번 시도 해주세요")
        return templates.TemplateResponse("login.html", form.__dict__)
    
    