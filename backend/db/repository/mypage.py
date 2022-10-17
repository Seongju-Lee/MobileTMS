from datetime import date, datetime, timedelta
from functools import reduce
import json
from math import dist
from os import access
from fastapi.encoders import jsonable_encoder
from numpy import product
from sqlalchemy import between, desc, distinct, not_, true 
from sqlalchemy.sql import func

from sqlalchemy.orm import Session

from db.models.kmodels import People, Yeon
from db.projects.project import ProjectTable
from db.models.users import Users
from db.logs.logs import AccessLog
from dateutil.relativedelta import relativedelta
import pandas as pd



def viewd_models(db: Session, user_id):


    print(user_id)
    models = db.query(AccessLog, People, Yeon, Users
            ).join(
                People, AccessLog.action == People.codesys
            ).join(
                Users, Users.rno == AccessLog.mem_idx
            ).outerjoin(
                Yeon, People.codesys == Yeon.codesys
            ).filter(
                (AccessLog.screen.contains('celeb-info') | AccessLog.screen.contains('model-info')) & (Users.id == user_id)
            ).group_by(
                AccessLog.action
            ).order_by(
                AccessLog.rno.desc()
            )

    

    return jsonable_encoder(models[:])




def viewd_projects(db: Session, user_id):
    
    projects = db.query(AccessLog, ProjectTable
            ).join(
                ProjectTable, AccessLog.action == ProjectTable.code
            ).join(
                Users, Users.rno == AccessLog.mem_idx
            ).filter(
                AccessLog.screen.contains('project-info') & (Users.id == user_id)
            ).group_by(
                AccessLog.action
            ).order_by(
                AccessLog.rno.desc()
            )

    

    return jsonable_encoder(projects[:])