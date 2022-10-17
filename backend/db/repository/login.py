from collections import UserString
from datetime import datetime
from numpy import insert
from sqlalchemy.orm import Session
from db.models.users import Users, Rusers
from fastapi.encoders import jsonable_encoder
from core.hashing import Hasher


def get_users(username: str, db: Session):
    
    user = db.query(Users).filter(Users.id == username)
    user_auth = ''
    
    if not jsonable_encoder(user[:]):
        isRuser = db.query(Rusers).filter(Rusers.uid == username)

        if jsonable_encoder(isRuser[:]):
            insert_user(jsonable_encoder(isRuser[:])[0]['uid'], jsonable_encoder(isRuser[:])[0]['upw'],  jsonable_encoder(isRuser[:])[0]['uname'], jsonable_encoder(isRuser[:])[0]['hp'], db)
        

    if jsonable_encoder(db.query(Rusers).filter(Rusers.uid == username)[:]):
        user_auth = jsonable_encoder(db.query(Rusers).filter(Rusers.uid == username)[:])[0]['webpower']
    
    return user, user_auth

def update_sms(username: str, hashed_auth_num:str ,db: Session):
    user = db.query(Users).filter(Users.id == username).first()
    user.last_auth = hashed_auth_num
    user.conn_time = datetime.now()
    db.commit()

def get_sms(username: str ,db: Session):
    sms_auth = db.query(Users.last_auth).filter(Users.id == username)
    return sms_auth 


def insert_user(id, password, name, phone, db:Session):
    print(id, password, name,phone)
    hashedpw = Hasher.get_hash_password(password)

    
    print('plain :: ', Hasher.verify_password(password, hashedpw))
    new_user = Users(username = name, id = id, hashed_password = hashedpw, phone=phone)
    db.add(new_user)
    db.commit()