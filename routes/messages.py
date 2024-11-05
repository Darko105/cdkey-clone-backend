from fastapi import APIRouter,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from datetime import datetime
from database import SessonLocal
from sqlalchemy.orm import Session
from helpers import get_db, db_dependency,user_exist


router = APIRouter()


class MessageResponseBase(BaseModel):
    id: int
    user_id:int
    title: str
    message_content:str
    date:str

class CreateMessageBase(BaseModel):
    title:str | None = None
    message_content: str | None = None



@router.post("/message/{user_id}",status_code=status.HTTP_201_CREATED)
async def create_message(user_id:int,data:CreateMessageBase,db:db_dependency):
    user_e = user_exist(user_id,db)
    if not user_e:
       raise HTTPException(status_code=404,detail="User Not Found!")
   
    message_data = models.Message(
       user_id=user_id,
       title=data.title,
       message_content=data.message_content,
       date=datetime.now()   
   )
   
    db.add(message_data)
    db.commit()
    db.refresh(message_data)
   
    return message_data

   
@router.get("/message/all/user/{user_id}",status_code=status.HTTP_200_OK)
async def get_messages(user_id:int,db:db_dependency):
    user_e = user_exist(user_id,db)
    if not user_e:
        raise HTTPException(status_code=404,detail="User Not Found!")
    get_messages_db = db.query(models.Message).filter(models.Message.user_id == user_id).all()
    if not get_messages_db:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    return get_messages_db