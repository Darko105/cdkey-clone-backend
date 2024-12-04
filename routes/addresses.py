from fastapi import APIRouter,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import SessonLocal
from sqlalchemy.orm import Session
from helpers import get_db, db_dependency


router = APIRouter()

class CreateBillingAddressBase(BaseModel):

    addresse1: str
    addresse2 : str | None = None
    city: str
    state: str
    zip_code: str
    country: str
    
    class Config:
        from_attributes = True

class ResponseBillingAddressBase(BaseModel):
    user_id:int
    book_id:int
    addresse1:str
    addresse2:str | None = None
    city:str
    state:str
    zip_code:str
    country:str
    
    class Config:
        from_attributes = True


@router.post("/users/{user_id}/billing-address",status_code=status.HTTP_201_CREATED)
async def create_billing_address(user_id:int,book:CreateBillingAddressBase,db:db_dependency):
    user_exits = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_exits:
        raise HTTPException(status_code=404,detail="User not Found!")
    
    db_user = models.BillingAddress(
        user_id = user_id,
        addresse1 = book.addresse1,
        addresse2 = book.addresse2,
        city = book.city,
        state = book.state,
        zip_code = book.zip_code,
        country = book.country,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return ResponseBillingAddressBase.model_validate(db_user)

@router.get("/users/{user_id}/billing-address",status_code=status.HTTP_200_OK)
async def get_billing_address(user_id:int,db:db_dependency):
    user_exist = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_exist:
        raise HTTPException(status_code=404,detail= "User Not Found!")
    
    db_book = db.query(models.BillingAddress).filter(models.BillingAddress.user_id == user_id).all()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="NO ADDRESSES FOUND!!!")
    
    return db_book


@router.delete("/users/{user_id}/billing-address/{book_id}",status_code=status.HTTP_200_OK)
async def delete_address(user_id:int,book_id,db:db_dependency):
    user_exist = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_exist:
        raise HTTPException(status_code=404,detail="User Not Found!")
    
    select_book = db.query(models.BillingAddress).filter(models.BillingAddress.user_id == user_id and models.BillingAddress.book_id == book_id).first()
    if not select_book:
        raise HTTPException(status_code=404,detail="No records was found!")
    

    db.delete(select_book)
    db.commit()
    
    return {"Message" : "Book deleted successfully"}
    
    
    
    
    
    