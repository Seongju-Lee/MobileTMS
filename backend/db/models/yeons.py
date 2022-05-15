from sre_compile import MAXCODE
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
    poom = Column(String(20))
    imonth = Column(Integer)
    fee = Column(Integer)
    dstart = Column(String(20))
    indefin = Column(String(20))
    nation = Column(String(20))
    writer = Column(String(20))
    wrdate = Column(String(20))



class RealTimeDRAMA(Base):
    __tablename__ = "yeondrama_nv"

    rno = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    drgubun = Column(String(20))
    drgubun2 = Column(String(20))
    title = Column(String(20))
    dstart = Column(String(20))
    rdate = Column(String(20))
    dend = Column(String(20))
    wrdate = Column(String(20))
    writer = Column(String(20))
    codesys = Column(String(20), ForeignKey("yeon.codesys"))
