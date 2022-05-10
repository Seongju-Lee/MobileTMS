from sre_compile import MAXCODE
from psycopg2 import Timestamp
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, TIMESTAMP, desc
from sqlalchemy.orm import relationship
from db.base_class import Base


class RealTimeCF(Base):
    __tablename__ = "yeoncf"

    rno = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    brand = Column(String(20))
    rdate = Column(String(20))
    dend = Column(String(20))
    codesys = Column(String(20), ForeignKey("yeon.codesys"))


# class RealTimePROC(Base):
#     __tablename__ = "mmeeting_proc"

#     rno = Column(Integer, primary_key=True)
#     edit_time = Column(TIMESTAMP)
#     projcode = Column(String(20))
#     mcode = Column(String(20), ForeignKey("yeon.codesys"))


class RealTimeDRAMA(Base):
    __tablename__ = "yeondrama_nv"

    rno = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    title = Column(String(20))
    rdate = Column(String(20))
    dend = Column(String(20))
    codesys = Column(String(20), ForeignKey("yeon.codesys"))
