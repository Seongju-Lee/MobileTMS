from collections import UserString
from sqlalchemy.orm import Session
from db.models.users import Users, User


def get_users(username: str, db: Session):
    print(username)
    user = db.query(Users).filter(Users.id == username)
    return user

def get_user(username: str, db: Session):
    user = db.query(User).filter(User.email == username)
    return user
