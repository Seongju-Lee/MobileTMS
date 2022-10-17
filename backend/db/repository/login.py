from collections import UserString
from datetime import datetime
from numpy import insert
from sqlalchemy.orm import Session
from db.models.users import Users


def get_users(username: str, db: Session):
    print(username)
    user = db.query(Users).filter(Users.id == username)
    return user

def update_sms(username: str, hashed_auth_num:str ,db: Session):
    user = db.query(Users).filter(Users.id == username).first()
    user.last_auth = hashed_auth_num
    user.conn_time = datetime.now()
    db.commit()

def get_sms(username: str ,db: Session):
    sms_auth = db.query(Users.last_auth).filter(Users.id == username)
    return sms_auth 