from datetime import date, datetime, timedelta
import json
from math import dist
from fastapi.encoders import jsonable_encoder
from sqlalchemy import between, desc, distinct, not_ 
from sqlalchemy.sql import func

from sqlalchemy.orm import Session

from db.models.kmodels import People, Mtel, ModelMov

from dateutil.relativedelta import relativedelta
 
# 모델 기본 상세정보
def model_info(db: Session, codesys: str = ''):
    print('before DB Access :: ' , codesys)

    model = db.query(
            People.codesys, People.mfee, People.name, People.sex, People.coname,  People.height, People.age, People.isyeon, People.sns2, People.insta_flw_str, People.dam, People.tel1, People.dam2, People.dam2tel, People.bun
        ).filter(
            People.codesys == codesys
        )
    return jsonable_encoder(model[:])



# 모델 통화내용 정보
def model_tel_memo(db: Session, codesys: str = ''):

    memo = db.query(
            Mtel.mcode, Mtel.edit_time ,Mtel.point2
        ).filter(
            Mtel.mcode == codesys
        )

    return jsonable_encoder(memo[:])


## 이미지영상
def mov_list(db: Session, codesys, mov_section: str):

    attachments_mov = {'img': 'AA영상', 'act': 'AA연기', 'cf': 'AA광고'}
    attachments_img = {'b': 'AA베스트사진', 'r': 'AA참고사진'}
    # print(attachments[0])
    try:
        if mov_section in attachments_mov.keys():
            return db.query(ModelMov.edit_time, ModelMov.mcode, ModelMov.fname, ModelMov.fext, ModelMov.fpath, ModelMov.fdate
                ).filter(
                    ModelMov.mcode == codesys
                ).filter(
                    ModelMov.fpath.contains(attachments_mov[mov_section])
                ).filter(
                    ModelMov.fext.contains('mp4')
                ).order_by(
                    desc(ModelMov.fdate)
                )

        elif mov_section in attachments_img.keys():
            return db.query(ModelMov.edit_time, ModelMov.mcode, ModelMov.fname, ModelMov.fext, ModelMov.fpath, ModelMov.fdate
                ).filter(
                    ModelMov.mcode == codesys
                ).filter(
                    ModelMov.fpath.contains(attachments_img[mov_section])
                ).filter(
                    ModelMov.fext.contains('jpg')
                ).order_by(
                    desc(ModelMov.fdate)
                )
        
    except:
        pass

# def img_mov_info(db: Session, codesys, ):
    
#     try:
#         return db.query(ModelMov.edit_time, ModelMov.mcode, ModelMov.fname, ModelMov.fext, ModelMov.fpath).filter(ModelMov.mcode == codesys).filter(ModelMov.fpath.contains('AA영상')).filter(ModelMov.fext.contains('mp4'))
#     except:
#         pass

## 연기영상
def act_mov_info(db: Session, codesys):
    
    try:
        return db.query(ModelMov.edit_time, ModelMov.mcode, ModelMov.fname, ModelMov.fext, ModelMov.fpath).filter(ModelMov.mcode == codesys).filter(ModelMov.fpath.contains('AA연기')).filter(ModelMov.fext.contains('mp4'))
    except:
        pass

## 연기영상
def cf_mov_info(db: Session, codesys):
    
    try:
        return db.query(ModelMov.edit_time, ModelMov.mcode, ModelMov.fname, ModelMov.fext, ModelMov.fpath).filter(ModelMov.mcode == codesys).filter(ModelMov.fpath.contains('AA광고')).filter(ModelMov.fext.contains('mp4'))

    except:
        pass

## 베스트사진
def best_img(db: Session, codesys):
    
    try:
        return db.query(ModelMov.edit_time, ModelMov.mcode, ModelMov.fname, ModelMov.fext, ModelMov.fpath).filter(ModelMov.mcode == codesys).filter(ModelMov.fpath.contains('AA베스트사진')).filter(ModelMov.fext.contains('jpg'))

    except:
        pass
