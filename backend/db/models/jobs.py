from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
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

class People(Base):
    no = Column(Integer, primary_key=True)
    codesys = Column(String(20))
    rdcode = Column(String(20))
    name = Column(String(20))
    age = Column(String(20))
    height = Column(String(20))
    sex= Column(String(20))
    