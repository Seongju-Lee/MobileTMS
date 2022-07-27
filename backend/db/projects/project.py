from datetime import date
from numpy import integer
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from db.base_class import Base


class ProjectTable(Base):
    __tablename__ = "project"



    no = Column(Integer,  primary_key=True)
    code = Column(String(20)) # project 코드
    edit_time = Column(TIMESTAMP)
    teamtag = Column(String(20)) # 담당 팀
    date = Column(String(20)) # 등록일, 작성일
    cfowner = Column(String(40)) # 광고주
    cfco = Column(String(100)) # 광고회사
    cfcotel = Column(String(30))
    cd = Column(String(100)) #CD
    cdtel = Column(String(100)) #CD TEL
    ae = Column(String(40)) # AE
    aetel = Column(String(40)) # AE TEL
    ae2 = Column(String(40)) # AE 2
    ae2tel = Column(String(40)) # AE TEL 2
    pd = Column(String(40)) # PD
    pdtel = Column(String(100)) # PD TEL
    media = Column(String(100)) # 매체
    gegigan = Column(String(100)) # 계약기간
    camsched = Column(String(100)) # 촬영일정
    feecom = Column(String(100)) # 모델료 지급사
    workercap = Column(String(100)) # 영업관리
    pdcomp = Column(String(100)) # PD컴퍼니
    pdcomptel = Column(String(100)) # PD컴퍼니 TEL

    onairck = Column(String(100)) # 온에어 날짜 


    pdcomppd1 = Column(String(100)) # PD컴퍼니 TEL
    pdcomppd1tel = Column(String(100)) # PD컴퍼니 TEL
    pdcomppd2 = Column(String(100)) # PD컴퍼니 TEL
    pdcomppd2tel = Column(String(100)) # PD컴퍼니 TEL
    pdcomppd3 = Column(String(100)) # PD컴퍼니 TEL
    pdcomppd3tel = Column(String(100)) # PD컴퍼니 TEL


    prod = Column(String(100)) # 프로덕션
    prodpdtel = Column(String(100)) # 프로덕션
    dir = Column(String(100)) # 감독
    dirtel = Column(String(100)) # 감독 TEL

    sdir1 = Column(String(100)) # 감독
    sdir1tel = Column(String(100)) # 감독 TEL


    seleb = Column(String(20)) # 셀럽건 확인 여부
    
    prname = Column(String(100)) # 프로젝트명
    
    boan19 = Column(String(100)) # 보안 프로젝트 - 기본 관리자만 접근 가능
    boan19ca = Column(String(100)) # 보안 프로젝트 - 지정된 팀만 접근 가능


    wktype = Column(String(100)) #  분류
    camdate = Column(String(100)) # 촬영일
    wktype2 = Column(String(100))
    camdate2 = Column(String(100))
    wktype3 = Column(String(100))
    camdate3 = Column(String(100))
    wktype4 = Column(String(100))
    camdate4 = Column(String(100))




class ProjectMemo(Base):
    __tablename__ = "projectpmemo"

    no = Column(Integer,  primary_key=True)
    code = Column(String(20)) # project 코드
    memo = Column(Text)


class ProjectContract(Base):
    __tablename__ = "money5"

    no = Column(Integer,  primary_key=True)
    code = Column(String(20)) # 모델코드
    projcode = Column(Text) # 프로젝트 코드
    cdate = Column(String(30)) # 촬영일
    mname = Column(String(30)) # 모델명
    modelfee = Column(Integer) # 모델료
    chunggu = Column(Integer) # 청구액
    poom = Column(String(30)) # 프로젝트명
    rdate = Column(String(30)) # 입력일
    susu = Column(Integer) # 수수료
    etc = Column(String(20)) # 비고
    geyakdate = Column(String(30)) # 계약일
    enddate = Column(String(30)) # 종료일
    geyakm = Column(String(30)) # 계약개월
    is_star = Column(String(20)) # 연예인


