from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from db.base_class import Base


class Users(Base):
    __tablename__ = "rmanager"

    rno = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    id = Column(String(20), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    phone = Column(String(20))
    last_auth = Column(String(20))
    conn_time = Column(TIMESTAMP)