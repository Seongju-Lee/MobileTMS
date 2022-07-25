from collections import UserString
from datetime import datetime
from numpy import insert
from sqlalchemy.orm import Session
from db.logs.logs import AccessLog
from db.models.users import Users
from fastapi.encoders import jsonable_encoder

def update_logs(username: str, ip, device, now, screen, db: Session):
    print(username)


    user = db.query(Users.rno).filter(Users.id == username).first()
    user = jsonable_encoder(user[:])[0]
    log = AccessLog(MEM_IDX=user, DEVICE=device, IP=ip, ACCESS_DATE=now, SCREEN=screen)
    db.add(log)
    db.commit()
    db.refresh(log)
    # user = db.query(AccessLog).filter(Users.id == username)
    return log