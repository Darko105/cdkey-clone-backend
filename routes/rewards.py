from fastapi import APIRouter,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from datetime import datetime
from database import SessonLocal
from sqlalchemy.orm import Session
from helpers import get_db, db_dependency,user_exist


router = APIRouter()

class RewordCreationBase(BaseModel):
    coin_balance:int

class RewordResponseBase(BaseModel):
    id:int | None = None
    user_id:int | None = None
    coin_balance:int 
        


@router.post("/rewards/{user_id}/add",status_code=status.HTTP_200_OK)
async def add_reword(user_id:int,reword:RewordCreationBase,db:db_dependency):
    user_exist(user_id,db)
    
    set_reword = models.Reword(
        user_id=user_id,
        coin_balance = reword.coin_balance,
    ) 
    
    db.add(set_reword)
    db.commit()
    db.refresh(set_reword)
    
    return set_reword


@router.get("/rewards/{user_id}",status_code=status.HTTP_200_OK)
async def get_rewords(user_id:int,db:db_dependency):
    user_e = user_exist(user_id,db)
    if not user_e:
        raise HTTPException(status_code=404,detail="User Not Found!")
    
    get_reword_db = db.query(models.Reword).filter(models.User.id == user_id).all()
    if not get_reword_db:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    return [RewordResponseBase.models_validate(item) for item in get_reword_db]

@router.get("/rewards",status_code=status.HTTP_200_OK)
async def get_all_reword(db:db_dependency):
    get_rewords_table = db.query(models.Reword).all()
    if not get_rewords_table:
        raise HTTPException(status_code=404,detail="Not Found!")
    
    return get_rewords_table

@router.put("/rewards/{user_id}/update",status_code=status.HTTP_201_CREATED)
async def update_reword(user_id:int,db:db_dependency):
    user_exist(user_id,db)
    
    pass