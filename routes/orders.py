from fastapi import APIRouter,HTTPException,status #,Depends
from pydantic import BaseModel
from typing import Annotated,Optional
import helpers
import models
# from database import SessonLocal
# from sqlalchemy.orm import Session
from datetime import datetime
from helpers import get_db, db_dependency, user_exist


router = APIRouter()


class OrderCreationBase(BaseModel):
    product_id:int
    product_img:str
    product_name:str
    user_id:int
    order_date:datetime
    key:str
    total_amount:str



@router.get("/users/{user_id}/orders",status_code=status.HTTP_200_OK)
async def get_all_orders(user_id:int,db:db_dependency):
    user = user_exist(user_id,db)
    if not user:
        raise HTTPException(status_code=404,detail="USER NOT FOUND!")
    orders = db.query(models.Order).filter(models.Order.user_id == user.id).all()
    
    return orders


@router.post("/users/{user_id}/orders",status_code=status.HTTP_200_OK)
async def get_all_orders(user_id:int,order:OrderCreationBase,db:db_dependency):
    user = user_exist(user_id,db)
    if not user:
        raise HTTPException(status_code=404,detail="USER NOT FOUND!")
    create_order = models.Order(
     
        product_id = order.product_id,
        key = order.key,
        user_id = user.id,
        order_date = order.order_date,
        total_amount = order.total_amount,
        product_name = order.product_name,
        product_img = order.product_img
    )
    
    db.add(create_order)
    db.commit()
    db.refresh(create_order)
    
    return {"message":"ORDER HAS BEEN ADDED SUCCESSFULY!"}
    