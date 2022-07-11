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
from db.projects.project import ProjectTable, ProjectMemo



 
def get_project(db: Session):
    
    a_project = db.query(ProjectTable)
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