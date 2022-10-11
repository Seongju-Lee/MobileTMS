from datetime import date, datetime, timedelta
import json
from math import dist
from fastapi.encoders import jsonable_encoder
from requests import session
from sqlalchemy import between, desc, distinct, not_ 
from sqlalchemy.sql import func

from sqlalchemy.orm import Session

from db.models.kmodels import People, Mtel, ModelMov, ModelCF, Memo, Yeon
from db.models.yeons import YeonCF
# from db.models.yeons import 
from dateutil.relativedelta import relativedelta
 
# 셀럽 기본 상세정보
def celeb_info(db: Session, codesys: str = ''):
    print('before DB Access :: ' , codesys)

    model = db.query(
            Yeon
        ).filter(
            Yeon.codesys == codesys
        )
    return jsonable_encoder(model[:])



# 모델 포인트 정보
def model_point_memo(db: Session, codesys: str = ''):

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


# 셀럽 광고이력
def get_celeb_cf(db: Session, codesys):

    cf_list = db.query(YeonCF
            ).filter(
                YeonCF.codesys == codesys
            ).filter(
                YeonCF.dend >= str(datetime.today().date()).replace('-', '.')
            ).order_by(
                desc(YeonCF.wrdate)
            )

    cf_list_end = db.query(YeonCF
            ).filter(
                YeonCF.codesys == codesys
            ).filter(
                YeonCF.dend < str(datetime.today().date()).replace('-', '.')
            ).order_by(
                desc(YeonCF.wrdate)
            )

    return jsonable_encoder(cf_list[:]), jsonable_encoder(cf_list_end[:])



# 모델 통화메모
def get_tel_memo(db: Session, codesys):
    memo_list = db.query(Memo
                ).filter(
                    Memo.code == codesys
                ).order_by(
                    desc(Memo.title)
                )

    return jsonable_encoder(memo_list[:])
