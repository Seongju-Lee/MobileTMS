from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from db.repository.search import search_job,  chu_30, movchoi, proc, order_register, order_recommend, order_s_count, order_read, search_celeb
# from db.repository.search import order_realtime, models_info, proc_celeb, img_mov_info, cf_mov_info, act_mov_info, best_img, get_rd_contracts
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.model import model_info, model_point_memo
from fastapi.encoders import jsonable_encoder
from striprtf.striprtf import rtf_to_text
from starlette.responses import RedirectResponse

import json

templates = Jinja2Templates(directory="templates")
router = APIRouter()

access_time = datetime.now()

@router.get("/mov/{mov_section}")
def get_mov_file(req: Request, codesys: str = '', mov_section: str = '',db: Session = Depends(get_db)):
    print('ghhhh', mov_section)