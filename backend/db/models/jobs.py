from ast import Str
from sre_compile import MAXCODE
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, TIMESTAMP, column, desc, Text
from sqlalchemy.orm import relationship
from db.base_class import Base


class Job(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(20), nullable=False)
    company = Column(String(20), nullable=False)
    company_url = Column(String(20))
    location = Column(String(20), nullable=False)
    description = Column(String(20))
    date_posted = Column(Date)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="jobs")


# 추천2022_ 30일추천 테이블
class Chu19(Base):
    __tablename__ = "chu19"

    rno = Column(Integer, primary_key=True)
    gubun = Column(String(20))
    edit_time = Column(TIMESTAMP)
    rdate = Column(String(20))
    jum = Column(Integer)
    mcode = Column(String(20), ForeignKey("people.codesys"))

    # chu = relationship("People", back_populates="people")


# 추천2022_ 30일추천 테이블
class Movsel(Base):
    __tablename__ = "movsel"

    rno = Column(Integer, primary_key=True)
    edit_time = Column(TIMESTAMP)
    mcode = Column(String(20), ForeignKey("people.codesys"))


# 추천2022_프로카운트 테이블
class Mmeeting_proc(Base):
    __tablename__ = "mmeeting_proc"

    rno = Column(Integer, primary_key=True)
    edit_time = Column(TIMESTAMP)
    projcode = Column(String(20))
    mcode = Column(String(20), ForeignKey("people.codesys"))
    s_mcode = Column(String(20), ForeignKey("yeon.codesys"))


# K-모델 테이블
class People(Base):
    __tablename__ = "people"

    no = Column(Integer)
    codesys = Column(String(20),  primary_key=True)
    rdcode = Column(String(20))
    name = Column(String(20))
    age = Column(String(20))
    height = Column(String(20))
    sex = Column(String(20))
    coname = Column(String(20))
    dam = Column(String(20))
    tel1 = Column(String(20))
    dam2 = Column(String(20))
    dam2tel = Column(String(20))
    dam3 = Column(String(20))
    dam3tel = Column(String(20))
    ptel = Column(String(20))
    sns2 = Column(String(20))
    insta_flw_str = Column(String(20))
    bun = Column(String(20))  # 학교
    mfee = Column(String(20))  # 모델료 (매칭 필요)
    isyeon = Column(String(20))
    # people = relationship("Chu19", back_populates="chu")
    # chu = Chu19


class People2(Base):
    no = Column(Integer,  primary_key=True)
    codesys = Column(String(20))
    bodysize = Column(String(20))
    mail1 = Column(String(100))


class Yeon(Base):
    __tablename__ = "yeon"

    rno = Column(Integer)
    codesys = Column(String(20),  primary_key=True)
    rdcode = Column(String(20))
    name = Column(String(20))
    age = Column(String(20))
    height = Column(String(20))
    sex = Column(String(20))
    a_3 = Column(Integer)
    a_6 = Column(Integer)
    a_12 = Column(Integer)


class Mtel(Base):
    __tablename__ = "mtel"

    no = Column(Integer,  primary_key=True)
    name = Column(String(20))
    mcode = Column(String(20), ForeignKey("people.codesys"))
    point2 = Column(Text)


class SunokStar(Base):
    __tablename__ = "model_sunokstar"

    rno = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    rcode = Column(String(20))
    mcode = Column(String(20), ForeignKey("yeon.codesys"))


class SunokStarChu(Base):
    __tablename__ = "model_sunokstar_chu"

    rno = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    frcode = Column(String(20), ForeignKey("model_sunokstar.rcode"))
    jum1 = Column(Integer)  # 추천
    jum2 = Column(Integer)  # 비추천


class SCount(Base):
    __tablename__ = "model_scelebida"

    rno = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    mcode = Column(String(20), ForeignKey("yeon.codesys"))


class Read(Base):
    __tablename__ = "rtqmodel"

    rno = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    rdate = Column(String(20))
    mcode = Column(String(20), ForeignKey("yeon.codesys"))


class Memo(Base):
    __tablename__ = "memo5"

    no = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    code = Column(String(20), ForeignKey("people.codesys"))
    rcode = Column(String(20))
    code2 = Column(String(20))
    code3 = Column(String(20))
    title = Column(String(20))
    memo = Column(String(20))
    # mcode = Column(String(20), ForeignKey("yeon.codesys"))


class Section(Base):
    __tablename__ = "tree"

    no = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    code = Column(String(20))
    title = Column(String(20))


class ModelCF(Base):
    __tablename__ = "modelcf"

    rno = Column(Integer,  primary_key=True)
    edit_time = Column(TIMESTAMP)
    rcode = Column(String(20))
    codesys = Column(String(20))
    rdjin = Column(String(20))
    indefin = Column(String(20))
    brand = Column(String(20))
    poom = Column(String(20))
    imonth = Column(Integer)
    fee = Column(Integer)
    dstart = Column(String(20))
    dend = Column(String(20))
    nation = Column(String(20))
    writer = Column(String(20))
    wrdate = Column(String(20))
