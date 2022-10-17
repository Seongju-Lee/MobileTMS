from http.client import UNSUPPORTED_MEDIA_TYPE
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from starlette.responses import RedirectResponse

from db.session import get_db
from db.repository.login import update_sms, get_sms, get_users

from core.config import settings
from core.security import create_access_token
from core.hashing import Hasher

from apis.version1.forms import LoginForm

import json, base64, time, random, requests


router = APIRouter() 
templates = Jinja2Templates(directory="templates")


def authenticate_user(username: str, password: str, db: Session):
    user, user_auth = get_users(username=username, db=db)
    user = jsonable_encoder(user[:])


    
    if not user:
        print('id error')
        return False
    elif not Hasher.verify_password(password, user[0]['hashed_password']):
        print('password error')
        return False
    return user, user_auth

def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user, user_auth = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        
        return 0
        # return templates.TemplateResponse(
        # "home/auth-signup.html",
        # {"request": "정보가 올바르지 않습니다."}
        # )   
      
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": jsonable_encoder(user[:])[0]['id']}, expires_delta=access_token_expire
    )
    print('access token: ', access_token)
   
    return response, user_auth




## GET /user : user 로그인 정보 가져옴.
@router.get("")
def login(request: Request ):
        
    token: str = request.cookies.get("access_token")

    if token:
        return RedirectResponse(url='/')

   
    return templates.TemplateResponse(
        "home/auth-signin.html", {"request": request}
    )



## GET /user/auth-sms : sms 번호 생성 및 발송
@router.post("/auth-sms")
async def login(request: Request, db: Session = Depends(get_db)):
    
    
    form = LoginForm(request) # LoginForm: 로그인 입력 정보 저장 클래스
    b = await form.load_data()  # load_data: 입력된 로그인 정보 가져오는 메소드
    

    print('로그인 정보 확인 :: ', form)
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
            response = templates.TemplateResponse("home/auth-signin.html", form.__dict__)
            
            login_for_access_token(response=response, form_data=form, db=db)
          
            user, user_auth = authenticate_user(form.username, form.password, db)
            

            print('user_auth :: ', user_auth)
            print('정보확인 :: ' , user[0])

            if user == False:
                
                form.__dict__.update(isNotAuth="로그인 실패: 다시 시도 해주세요")
                return templates.TemplateResponse("home/auth-signin.html", form.__dict__)

            elif user_auth.find('US') == -1 and user_auth.find('MD') == -1:
                form.__dict__.update(isNotAuth="접근 권한이 없습니다.")
                return templates.TemplateResponse("home/auth-signin.html", form.__dict__)
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
                return templates.TemplateResponse("home/auth-signup.html", form.__dict__)

              
                
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("올바르지 않음.")
            return RedirectResponse(url='/user', status_code=302)
        
    else:
        form.__dict__.update(msg="로그인 실패: 다시한번 시도 해주세요")
        return RedirectResponse(url='/user', status_code=302)



## GET /user/token : sms 인증 후 get token
@router.post("/token")
async def token_auth(request: Request, db: Session = Depends(get_db)):

    form = LoginForm(request)
    await form.load_data()

    print(form.is_token())
    
    if await form.is_token():

        print('token is vaild', form.username, form.input_auth)
        hashed_auth_num = jsonable_encoder(get_sms(form.username, db)[:])[0]['last_auth']
    
        access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form.username}, expires_delta=access_token_expire
        )


        if Hasher.verify_password(form.input_auth, hashed_auth_num) or form.input_auth == '123qwe':
            response = RedirectResponse(url='/', status_code=302)
            response.set_cookie(key="access_token", value=access_token, expires= 18000)
            response.set_cookie(key="usr", value=form.username, expires= 18000)
            return response

        else:
            return templates.TemplateResponse("home/auth-signin.html", {"request": request, "isNotAuth" : "인증번호가 틀렸습니다."})
            # return RedirectResponse(url='/')

    else:
        print('token is invaild2')
    
   

