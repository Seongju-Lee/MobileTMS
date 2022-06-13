from pydoc import resolve
from ssl import ALERT_DESCRIPTION_ACCESS_DENIED, AlertDescription
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
from requests.auth import HTTPBasicAuth
import base64
import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import random

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")




user_id = ''
user_rno = ''



def token(user_phone: str='', user_id: str='',  access_token: str=''):


    response = RedirectResponse(url='/v1' )
    response.set_cookie(key="access_token", value=access_token, expires= 10800)
    return response
  

@router.get("/auth")
def token_auth(input_auth: str='', user_id: str='', db: Session = Depends(get_db)):
    print('sms: ', input_auth)
    
    print('user-id: ', user_id)

    hashed_auth_num = jsonable_encoder(get_sms(user_id, db)[:])[0]['last_auth']
    
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expire
    )

    response = RedirectResponse(url='/', status_code=302)
    response.set_cookie(key="access_token", value=access_token, expires= 10800)

    if Hasher.verify_password(input_auth, hashed_auth_num):
        print('동일')
        return response
    else:
        return RedirectResponse(url='/login')


# @router.post("/v1")
# def sms_auth(request: Request):
#     return templates.TemplateResponse("sms_auth.html", {"request": request})

@router.get("/login")
def login(request: Request, msg: str = None):
    print('param msg확인: ', msg)
    return templates.TemplateResponse(
        "login.html", {"request": request, "msg": msg}
    )


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):

    form = LoginForm(request)
    await form.load_data() 

    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    
    with open("api_sms.json", 'r', encoding='utf-8') as json_file:
        sms_api = json.load(json_file)
        
        access_key = sms_api['ACCESS_KEY']
        
        secret_key = sms_api['SECRET_KEY'] # access key id (from portal or Sub Account)
    access_key = access_key
    secret_key = secret_key

    url = 'https://sens.apigw.ntruss.com'
    uri = '/sms/v2/services/ncp:sms:kr:287156821959:sms_test/messages'
    
    ########## 키 생성 함수
    def make_signature(secret_key, access_key):
        
        secret_key = bytes(secret_key, 'UTF-8')
        method = "POST"
        message = method + " " + uri + '\n' + timestamp + '\n' + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey


    if await form.is_valid():
        try:
            # form.__dict__.update(msg="Login Successful")
            response = templates.TemplateResponse("login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            print('token접근: ', login_for_access_token(response=response, form_data=form, db=db))


            user = authenticate_user(form.username, form.password, db)
            print('user임: ', user)
            if user == False:

                form.__dict__.update(msg="로그인 실패: 다시 시도 해주세요")
                return templates.TemplateResponse("login.html", form.__dict__)

                # return response
            else:
               
                # try: # 로그인 성공
                # 문자 인증 이동.

                auth_num = random.randint(100000,999999)

                header = {
                "Content-Type" : "application/json; charset=utf-8",
                "x-ncp-apigw-timestamp" : timestamp,
                "x-ncp-iam-access-key" : access_key,
                "x-ncp-apigw-signature-v2" : make_signature(secret_key, access_key)
                }

                data = {
                    "type":"SMS",
                    "from":"01037038419",
                    "subject":"발신번호테스트",
                    "content":"[레디 모바일TMS] 인증번호 [{}]를 입력해주세요.".format(auth_num),
                    "messages":[
                        {
                        "to":user[:][0]['phone'],
                        }
                    ]
                }

                
                # 인증번호 생성 및 저장  // 유저 정보 저장
              

                hashed_auth_num = Hasher.get_hash_password(str(auth_num))
                update_sms((user[:])[0]['id'], hashed_auth_num, db=db)
                res= requests.post(url=(url+uri),headers=header,data=json.dumps(data))
                print(res.json())

                # 문자인증 페이지로 이동.
                form.__dict__.update(msg={'user_id' : (user[:])[0]['id']})
                return templates.TemplateResponse("sms_auth.html", form.__dict__)


                # except:
                #     form.__dict__.update(msg="sms error")
                #     return templates.TemplateResponse("login.html", form.__dict__)
                    
                # print((datetime.utcnow() + timedelta(minutes=1)))
                # return response
                
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("올바르지 않음.")

            return templates.TemplateResponse("login.html", form.__dict__)
        
    else:
        form.__dict__.update(msg="로그인 실패: 다시한번 시도 해주세요")
        return templates.TemplateResponse("login.html", form.__dict__)
    
    


# @router.post("/sms")
# def sms_auth_(user_phone: str='', user_id: str=''):
#     return templates.TemplateResponse("sms_auth.html", {"request": 'tmp'})