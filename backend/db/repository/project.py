from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, not_

from sqlalchemy.orm import Session
from db.projects.project import ProjectTable, ProjectMemo, ProjectContract, ProjectFile
from db.models.kmodels import People
from db.models.users import Users, Rusers
from sqlalchemy.sql import func

from datetime import datetime
from dateutil.relativedelta import relativedelta

 
# kmodel 상세정보: 레디진행 프로젝트 목록 
def get_kmodel_project(db: Session, mcode : str = ''):
    project_list = db.query(ProjectContract).filter(ProjectContract.code == mcode).order_by(desc(ProjectContract.cdate))

    return jsonable_encoder(project_list[:])


# 기본 프로젝트 리스트 : 최신 등록 순 
def get_project(db: Session):
    
    a_project = db.query(ProjectTable).order_by(ProjectTable.date.desc()).limit(300)
    return a_project



# 프로젝트 검색 필터 적용
def get_filter_project(db: Session, teamtag, prname, cfowner, cfcompany, pryear):


    
    projects = db.query(ProjectTable
                ).filter(
                    ([ProjectTable.teamtag.contains(teamtag), ProjectTable.teamtag.contains('')][teamtag=='All']) & ProjectTable.prname.contains(prname) & (ProjectTable.cfowner.contains(cfowner) | ProjectTable.dir.contains(cfowner) | ProjectTable.sdir1.contains(cfowner) | ProjectTable.pd.contains(cfowner) | ProjectTable.ae.contains(cfowner) | ProjectTable.ae2.contains(cfowner) | ProjectTable.cd.contains(cfowner) | ProjectTable.pdcomppd1.contains(cfowner) | ProjectTable.pdcomppd2.contains(cfowner) | ProjectTable.pdcomppd3.contains(cfowner) | ProjectTable.prodpd.contains(cfowner) | ProjectTable.sdir2.contains(cfowner))
                    & (ProjectTable.cfco.contains(cfcompany) | ProjectTable.cfowner.contains(cfcompany) | ProjectTable.pdcomp.contains(cfcompany) | ProjectTable.pdcomppd1.contains(cfcompany)| ProjectTable.pdcomppd2.contains(cfcompany) | ProjectTable.pdcomppd3.contains(cfcompany) | ProjectTable.prod.contains(cfcompany) | ProjectTable.pdcomppd3.contains(cfcompany))
                    & (func.left(ProjectTable.date, 4).in_(pryear))
                ).order_by(
                    ProjectTable.date.desc()
                ).limit(350)

    return projects


# 프로젝트 상세 기본정보~연락처까지
def get_project_information(db: Session, pcode):
    info = db.query(ProjectTable).filter(ProjectTable.code == pcode)
    return info

# 첨부파일
def get_project_file(db: Session, pcode):

    files = db.query(ProjectFile.dir, ProjectFile.dir2, func.group_concat(ProjectFile.fname).label('fnames')
            ).filter(ProjectFile.rootdir.contains(pcode)
            ).group_by(ProjectFile.dir
            ).order_by(ProjectFile.dir.desc())


    print(files)

    return files










# 프로젝트 필터검색 공통항목
def query_filter_project(f_project, project_name, rd_team, cf_owner, cf_co, cf_regdate):
    f_project = f_project.filter(ProjectTable.prname.contains(project_name) &
    (ProjectTable.dir.contains(cf_owner) | ProjectTable.sdir1.contains(cf_owner) | ProjectTable.pd.contains(cf_owner) | ProjectTable.ae.contains(cf_owner) | ProjectTable.ae2.contains(cf_owner) | ProjectTable.cd.contains(cf_owner) | ProjectTable.pdcomppd1.contains(cf_owner) | ProjectTable.pdcomppd2.contains(cf_owner) | ProjectTable.pdcomppd3.contains(cf_owner) | ProjectTable.prodpd.contains(cf_owner) | ProjectTable.sdir2.contains(cf_owner))& 
    (ProjectTable.cfco.contains(cf_co) | ProjectTable.cfowner.contains(cf_co) | ProjectTable.pdcomp.contains(cf_co) | ProjectTable.pdcomppd1.contains(cf_co)| ProjectTable.pdcomppd2.contains(cf_co) | ProjectTable.pdcomppd3.contains(cf_co) | ProjectTable.prod.contains(cf_co) | ProjectTable.pdcomppd3.contains(cf_co))&
    ProjectTable.date.contains(cf_regdate))

    return f_project


# def get_filter_project(db: Session, project_name, rd_team, cf_owner, cf_co, cf_regdate, isceleb):

#     f_project = [(db.query(ProjectTable).filter(ProjectTable.teamtag.contains(rd_team) & not_(ProjectTable.seleb.contains('V')))), db.query(ProjectTable).filter( not_(ProjectTable.seleb.contains('V'))) ][rd_team=='전체'] if isceleb == 'n' else [(db.query(ProjectTable).filter(ProjectTable.teamtag.contains(rd_team) &
#             ProjectTable.seleb.contains(isceleb))), db.query(ProjectTable).filter(ProjectTable.seleb.contains(isceleb))][rd_team=='전체']
    
#     f_project = query_filter_project(f_project, project_name, rd_team, cf_owner, cf_co, cf_regdate, isceleb)
#     return f_project


def get_project_memo(db: Session, pcode):
    memo = db.query(ProjectMemo).filter(ProjectMemo.code == pcode)
    return memo

def get_project_model(db: Session, projcode):
    models = db.query(ProjectContract).filter(ProjectContract.projcode == projcode)
    return models


def get_project_with(db: Session, entertainment):

    ############## 소속 연예인 리스트 ############
    codes = []
    entertainment_models = db.query(People.codesys).filter(People.coname.contains(entertainment))

    for code in jsonable_encoder(entertainment_models[:]):
        codes.append(code['codesys'])
    
    ############################

    ############# 소속 연예인들 레디 진행 이력 리스트 ##############

    project_table = []

    for model in codes:
        projects = db.query(ProjectContract).filter(ProjectContract.code == model).filter(ProjectContract.cdate >= (datetime.today() - relativedelta(months=36)))
        projects = jsonable_encoder(projects[:])

        for project in projects:
            if (project['modelfee']):
                project['modelfee'] = format(project['modelfee'], ',')
            
            if project['susu']:  
                project['susu'] =format(project['susu'], ',')
            if project['chunggu']:
                project['chunggu'] = format(project['chunggu'], ',')
            project_table.append(project)

    
    return project_table

## 보안 프로젝트 일 경우만 call
def project_security(db: Session, user_id, pcode, team_scrty, admin_scrty):

    user_auth = db.query(RUsers.team, RUsers.power8).filter(RUsers.uid == user_id)

    try:
        user_auth = jsonable_encoder(user_auth[:])[0]


        if (user_auth['team'] in team_scrty) or ('PBO' in user_auth['power8']):
            return 1
        else:
            return 0
    except:
        return 'fail'
