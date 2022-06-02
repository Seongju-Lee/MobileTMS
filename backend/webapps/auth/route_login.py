from pydoc import resolve
from ssl import AlertDescription
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from webapps.auth.forms import LoginForm
from apis.version1.route_login import login_for_access_token, authenticate_user
from starlette.responses import RedirectResponse

from core.config import settings
from datetime import datetime, timedelta
from core.security import create_access_token
from fastapi.encoders import jsonable_encoder

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")



@router.get("/login")
def login(request: Request, msg: str = None):
    return templates.TemplateResponse(
        "login.html", {"request": request, "msg": msg}
    )


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data() 

    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful")
            response = templates.TemplateResponse("login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            print('token접근: ', login_for_access_token(response=response, form_data=form, db=db))


            user = authenticate_user(form.username, form.password, db)
            print('user임: ', user)
            if user == False:

                response = RedirectResponse(url='/login', status_code=302)
                return response
            else:
                access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": jsonable_encoder(user[:])[0]['id']}, expires_delta=access_token_expire
                )
                print('access token: ', access_token)
                try:
                    response = RedirectResponse(url='/', status_code=302)
                    response.set_cookie(key="access_token", value=access_token, expires= 10800)

                except:
                    response = RedirectResponse(url='/login', status_code=302)
                # response.set_cookie(key="access_tkn", value=f"Bearer {access_token}")
                print((datetime.utcnow() + timedelta(minutes=1)))
                return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("올바르지 않음.")
            return templates.TemplateResponse("login.html", form.__dict__)
        
    return templates.TemplateResponse("login.html", form.__dict__)
