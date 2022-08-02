from ast import expr_context
from asyncore import write
from curses import reset_prog_mode
from datetime import date, datetime, timedelta
import imp
import json
from mmap import mmap
from ntpath import join
from pickle import PERSID
from statistics import mode
from tkinter import HIDDEN
from xmlrpc.server import SimpleXMLRPCRequestHandler
from fastapi.encoders import jsonable_encoder
from numpy import sort
from sqlalchemy import between, desc, false, not_, true
from sqlalchemy.sql.expression import func

from sqlalchemy.orm import Session
# from schemas.jobs import JobCreate
from db.projects.project import ProjectTable, ProjectMemo, ProjectContract
from db.models.kmodels import People
from db.models.users import Users, RUsers

from datetime import datetime
from dateutil.relativedelta import relativedelta

 
def get_project(db: Session):
    
    a_project = db.query(ProjectTable).order_by(ProjectTable.date.desc()).limit(300)
    
    return a_project


def get_filter_project(db: Session, project_name, rd_team, cf_owner, cf_co, cf_regdate, isceleb):
    

    if isceleb == 'n':
        if rd_team == '전체':
            
            f_project = db.query(ProjectTable).filter(ProjectTable.prname.contains(project_name) & not_(ProjectTable.seleb.contains('V'))&
            (ProjectTable.dir.contains(cf_owner) | ProjectTable.sdir1.contains(cf_owner) | ProjectTable.pd.contains(cf_owner) | ProjectTable.ae.contains(cf_owner) | ProjectTable.ae2.contains(cf_owner) | ProjectTable.cd.contains(cf_owner) | ProjectTable.pdcomppd1.contains(cf_owner) | ProjectTable.pdcomppd2.contains(cf_owner) | ProjectTable.pdcomppd3.contains(cf_owner) | ProjectTable.prodpd.contains(cf_owner) | ProjectTable.sdir2.contains(cf_owner)) 
            & ProjectTable.cfco.contains(cf_co) & ProjectTable.date.contains(cf_regdate))
        else:
            f_project = db.query(ProjectTable).filter(ProjectTable.prname.contains(project_name) &  not_(ProjectTable.seleb.contains('V')) &
            (ProjectTable.dir.contains(cf_owner) | ProjectTable.sdir1.contains(cf_owner) | ProjectTable.pd.contains(cf_owner) | ProjectTable.ae.contains(cf_owner) | ProjectTable.ae2.contains(cf_owner) | ProjectTable.cd.contains(cf_owner) | ProjectTable.pdcomppd1.contains(cf_owner) | ProjectTable.pdcomppd2.contains(cf_owner) | ProjectTable.pdcomppd3.contains(cf_owner) | ProjectTable.prodpd.contains(cf_owner) | ProjectTable.sdir2.contains(cf_owner)) 
            & ProjectTable.cfco.contains(cf_co) & ProjectTable.date.contains(cf_regdate))

    else:

        if rd_team == '전체':
            f_project = db.query(ProjectTable).filter(ProjectTable.prname.contains(project_name) & ProjectTable.seleb.contains(isceleb) &
            (ProjectTable.dir.contains(cf_owner) | ProjectTable.sdir1.contains(cf_owner) | ProjectTable.pd.contains(cf_owner) | ProjectTable.ae.contains(cf_owner) | ProjectTable.ae2.contains(cf_owner) | ProjectTable.cd.contains(cf_owner) | ProjectTable.pdcomppd1.contains(cf_owner) | ProjectTable.pdcomppd2.contains(cf_owner) | ProjectTable.pdcomppd3.contains(cf_owner) | ProjectTable.prodpd.contains(cf_owner) | ProjectTable.sdir2.contains(cf_owner))
            & ProjectTable.cfco.contains(cf_co) & ProjectTable.date.contains(cf_regdate))
        else:
            f_project = db.query(ProjectTable).filter(ProjectTable.prname.contains(project_name) & ProjectTable.teamtag.contains(rd_team) &
            ProjectTable.seleb.contains(isceleb) & (ProjectTable.dir.contains(cf_owner) | ProjectTable.sdir1.contains(cf_owner) | ProjectTable.pd.contains(cf_owner) | ProjectTable.ae.contains(cf_owner) | ProjectTable.ae2.contains(cf_owner) | ProjectTable.cd.contains(cf_owner) | ProjectTable.pdcomppd1.contains(cf_owner) | ProjectTable.pdcomppd2.contains(cf_owner) | ProjectTable.pdcomppd3.contains(cf_owner) | ProjectTable.prodpd.contains(cf_owner) | ProjectTable.sdir2.contains(cf_owner))
            & ProjectTable.cfco.contains(cf_co) & ProjectTable.date.contains(cf_regdate))
        
   
    return f_project


def get_project_info(db: Session, pcode):
    

    info = db.query(ProjectTable).filter(ProjectTable.code == pcode)
    return info

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
        print(' 유저 권한 확인 :: ' , jsonable_encoder(user_auth[:]))
        user_auth = jsonable_encoder(user_auth[:])[0]


        if (user_auth['team'] in team_scrty) or ('PBO' in user_auth['power8']):
            return 1
        else:
            return 0
    except:
        return 'fail'
    


