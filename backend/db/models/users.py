from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(20), unique=True, nullable=False, index=True)
    hashed_password = Column(String(80), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    jobs = relationship("Job", back_populates="owner")


class Users(Base):
    __tablename__ = "rmanager"

    rno = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    id = Column(String(20), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    phone = Column(String(20))
    last_auth = Column(String(20))
    conn_time = Column(TIMESTAMP)