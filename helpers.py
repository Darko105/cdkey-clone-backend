from typing import Annotated
from fastapi import Depends
from passlib.context import CryptContext
from requests import Session
from database import SessonLocal
import models

#hashing user password 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


#get database else or close the connection

def get_db():
    db = SessonLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency= Annotated[Session, Depends(get_db)]


def user_exist(user_id:int,db):
    res = db.query(models.User).filter(models.User.id == user_id).first()
    return res