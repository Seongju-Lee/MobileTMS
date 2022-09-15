from datetime import date, datetime, timedelta
import json
from fastapi.encoders import jsonable_encoder
from sqlalchemy import between, desc, not_

from sqlalchemy.orm import Session

from db.models.kmodels import  People2
from db.models.kmodels import People, Chu19, Movsel, Mmeeting_proc, Yeon, SunokStar, SunokStarChu, SCount, Read, Mtel, Memo, Section, ModelCF, ModelMov
from db.models.yeons import RealTimeCF, RealTimeDRAMA
from db.projects.project import ProjectContract

from dateutil.relativedelta import relativedelta
 

def search_test(db: Session):
    
    models = db.query(People)
    print(len(jsonable_encoder(models[:])))

    return jsonable_encoder(models[:])