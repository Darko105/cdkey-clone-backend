from fastapi import APIRouter,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import SessonLocal
from sqlalchemy.orm import Session
from helpers import get_db


router = APIRouter()

class CreateBillingAddress(BaseModel):

    addresse1: str
    addresse2 : str | None = None
    city: str
    state: str
    zip_code: str
    country: str
    
    class Config:
        from_attributes = True


db_dependency= Annotated[Session, Depends(get_db)]

@router.post("/add-billing-address/{user_id}",status_code=status.HTTP_201_CREATED)
async def create_billing_address(user_id:int,book:CreateBillingAddress,db:db_dependency):
    user_exits = db.query(models.User).filter(models.User.id == user_id).first()
    if user_exits is None:
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

    return db_user