import http
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import APIRouter
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
templates = Jinja2Templates(directory="templates")


def authenticate_user(username: str, password: str, db: Session):
    user = get_users(username=username, db=db)
    print('user 확인: ', jsonable_encoder(user[:]))
    user = jsonable_encoder(user[:])

    if not user:
        print('id error')
        return False
    elif not Hasher.verify_password(password, user[0]['hashed_password']):
        print('password error')
        return False
    return user


@router.post("/token")
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        return templates.TemplateResponse(
        "login.html",
        {"request": "정보가 올바르지 않습니다."}
        )   
      
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": jsonable_encoder(user[:])[0]['id']}, expires_delta=access_token_expire
    )
    print('access token: ', access_token)
    print('access token: ', datetime.utcnow() + timedelta(minutes=1))
   
    return response

