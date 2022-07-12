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
from sqlalchemy import between, desc, not_
from sqlalchemy.sql.expression import func

from sqlalchemy.orm import Session
# from schemas.jobs import JobCreate
from db.projects.project import ProjectTable, ProjectMemo, ProjectContract
from db.models.kmodels import People
from datetime import datetime
from dateutil.relativedelta import relativedelta

 
def get_project(db: Session):
    
    a_project = db.query(ProjectTable).order_by(ProjectTable.date.desc()).limit(100)
    
    return a_project


def get_filter_project(db: Session, project_name, rd_team, cf_owner, cf_regdate, isceleb):
    

    if isceleb == 'n':
        if rd_team == '전체':
            
            f_project = db.query(ProjectTable).filter(ProjectTable.prname.contains(project_name) & not_(ProjectTable.seleb.contains('V'))&
            ProjectTable.cfowner.contains(cf_owner) & ProjectTable.date.contains(cf_regdate))
        else:
            f_project = db.query(ProjectTable).filter(ProjectTable.prname.contains(project_name) &  not_(ProjectTable.seleb.contains('V')) &
            ProjectTable.cfowner.contains(cf_owner) & ProjectTable.date.contains(cf_regdate))

    else:

        if rd_team == '전체':
            f_project = db.query(ProjectTable).filter(ProjectTable.prname.contains(project_name) & ProjectTable.seleb.contains(isceleb) &
            ProjectTable.cfowner.contains(cf_owner) & ProjectTable.date.contains(cf_regdate))
        else:
            f_project = db.query(ProjectTable).filter(ProjectTable.prname.contains(project_name) & ProjectTable.teamtag.contains(rd_team) &
            ProjectTable.seleb.contains(isceleb) & ProjectTable.cfowner.contains(cf_owner) & ProjectTable.date.contains(cf_regdate))
        
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
    # for i in project_table:
    #     print( '프로젝트 테이블 구성 :: ' , i)

    # search_project = db.query(ProjectContract).filter(ProjectContract.)
