from code import interact
from sre_compile import MAXCODE
from sqlalchemy import Column, ColumnDefault, Integer, String, Date, Boolean, ForeignKey, TIMESTAMP, desc
from sqlalchemy.orm import relationship
from db.base_class import Base


# 실베스타 - 계약현황 테이블
class YeonCF(Base):
    __tablename__ = "yeoncf"

    rno = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    brand = Column(String(20))
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

# 실베스타 - 활동내역 테이블
class ContractDrama(Base):
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

# S카운트 얻고, 모델코드(mcode) 확인 위한 테이블
class ScountId(Base):
    __tablename__ = "model_scelebida"

    rno = Column(Integer,  primary_key=True)

    frcode = Column(String(50))
    rdate = Column(String(50))
    rcode = Column(String(50))
    mcode = Column(String(50))


# 순옥스타 테이블
class SunokStar(Base):
    __tablename__ = "model_sunokstar"

    rno = Column(Integer,  primary_key=True)
    rcode = Column(String(50))
    mcode = Column(String(50))
    mcode2 = Column(String(50))
    mcode3 = Column(String(50))
    mcode4 = Column(String(50))
    mea = Column(Integer)
    suntitle = Column(String(50))



# 순옥스타 추천순
class SunokStarRecommend(Base):
    __tablename__ = "model_sunokstar_chu"

    rno = Column(Integer,  primary_key=True)
    rcode = Column(String(50))
    frcode = Column(String(50))
    jum1 = Column(Integer)
    jum2 = Column(Integer)
