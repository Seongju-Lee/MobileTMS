from psycopg2 import Timestamp
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, TIMESTAMP, desc
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


# 추천2022_프로카운트 테이블
class Mmeeting_proc(Base):
    __tablename__ = "mmeeting_proc"

    rno = Column(Integer, primary_key=True)
    edit_time = Column(TIMESTAMP)
    projcode = Column(String(20))
    mcode = Column(String(20), ForeignKey("people.codesys"))


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

    # people = relationship("Chu19", back_populates="chu")
    # chu = Chu19


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
