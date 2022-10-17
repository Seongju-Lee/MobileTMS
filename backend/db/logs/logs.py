from datetime import date
from numpy import integer
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from db.base_class import Base


class AccessLog(Base):
    __tablename__ = "temp2"


    rno = Column(Integer,  primary_key=True)
    mem_idx = Column(Integer) # 사용자 ID
    device = Column(String(255)) # 접속 장치
    ip = Column(String(100)) # 접속 IP
    access_time = Column(TIMESTAMP) # 접속 시간
    action = Column(String(100)) # 접속 route
    screen = Column(String(100)) # 접속 화면






