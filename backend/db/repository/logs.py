from collections import UserString
from datetime import datetime
from numpy import insert
from sqlalchemy.orm import Session
from db.logs.logs import AccessLog
from db.models.users import Users
from fastapi.encoders import jsonable_encoder

def update_logs(username: str, ip, device, now, screen, db: Session, action: str = ''):
    
    print(username)

    user = db.query(Users.rno).filter(Users.id == username).first()
    user = jsonable_encoder(user[:])[0]
    
    if action:
        log = AccessLog(mem_idx=user, device=device, ip=ip, access_time=now, screen=screen, action=action)
    else:
        log = AccessLog(mem_idx=user, device=device, ip=ip, access_time=now, screen=screen)

    db.add(log)
    db.commit()
    db.refresh(log)

    return log