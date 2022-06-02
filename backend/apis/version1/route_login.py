from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from apis.utils import OAuth2PasswordBearerWithCookie
from fastapi import Depends
from fastapi import APIRouter, HTTPException, status
from db.session import get_db
from sqlalchemy.orm import Session
from core.config import settings
from datetime import timedelta
from core.security import create_access_token
from db.repository.login import get_user, get_users
from core.hashing import Hasher
from jose import jwt, JWTError
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def authenticate_user(username: str, password: str, db: Session):
    user = get_users(username=username, db=db)
    print('user 확인: ', jsonable_encoder(user[:]))
    # print('해쉬요~  ', password,'  ',Hasher.get_hash_password(password))
    print(Hasher.verify_password(password, user[0].hashed_password))
    if not user:
        return False
    if not Hasher.verify_password(password, user[0].hashed_password):
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
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Invalid username or password",
        # )
    # print(jsonable_encoder(user[:])[0]['uid'])
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": jsonable_encoder(user[:])[0]['id']}, expires_delta=access_token_expire
    )
    print('access token: ', access_token)
    print('access token: ', datetime.utcnow() + timedelta(minutes=1))
    # response.set_cookie(key="access_tkn", value=f"Bearer {access_token}")
    # response.set_cookie(key="access_tkn", value=access_token, expires= (datetime.utcnow() + timedelta(minutes=1)) )
    
    # return {"access_token": access_token, "token_type": "bearer"}
    return response


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user
