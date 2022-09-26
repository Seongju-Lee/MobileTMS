from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP,  Text
from sqlalchemy.orm import relationship
from db.base_class import Base


class Users(Base):
    __tablename__ = "rmanager"

    rno = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    id = Column(String(20), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    team = Column(String(20))
    
    phone = Column(String(20))
    last_auth = Column(String(20))
    conn_time = Column(TIMESTAMP)



class Rusers(Base):
    __tablename__ = "ruser"

    uid = Column(Integer, primary_key=True)
    team = Column(String(20), nullable=False)
    power8 = Column(String(Text), nullable=False)
   