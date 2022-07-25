from datetime import date
from numpy import integer
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from db.base_class import Base


class AccessLog(Base):
    __tablename__ = "temp1"


    idx = Column(Integer,  primary_key=True)
    MEM_IDX = Column(Integer) # 모델코드
    DEVICE = Column(String(255)) # 프로젝트 코드
    IP = Column(String(100)) # 촬영일
    ACCESS_DATE = Column(TIMESTAMP) # 모델명
    SCREEN = Column(String(100)) # 모델료
    ACTION = Column(String(100)) # 모델료





