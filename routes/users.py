from fastapi import APIRouter,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated,Optional
import helpers
import models
from database import SessonLocal
from sqlalchemy.orm import Session
from datetime import datetime
from helpers import get_db, db_dependency


router = APIRouter()

class UserCreateBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    password: str

class UpdateUserInformationBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    


class UserResponseBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    staff: bool
    created: datetime
    updated: datetime
    is_active: bool

    class Config:
        from_attributes = True
        
        



@router.post("/users",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateBase, db:db_dependency):
    user_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already exist.!")
    
    hashed_password = helpers.hash_password(user.password)
    current_time = datetime.now()
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email, 
        phone_number=user.phone_number,
        password=hashed_password,
        created=current_time,
        updated=current_time,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponseBase.model_validate(db_user)



@router.get("/users/{user_id}",status_code=status.HTTP_200_OK)
async def get_user(user_id:int,db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User Not Found!")
    return UserResponseBase.model_validate(user)



@router.get("/getallusers",response_model=list[UserResponseBase],status_code=status.HTTP_200_OK)
async def get_all_users(db:db_dependency):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404,detail="not autherised or found!")
    return [UserResponseBase.model_validate(item) for item in users]

@router.put("/update-user/{user_id}",status_code=status.HTTP_200_OK)
async def update_user(user_id:int,user:UpdateUserInformationBase,db:db_dependency):
    print(user)
    user_exist = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_exist:
        raise HTTPException(status_code=404,detail="User Not Found!")
    update_data = user.dict(exclude_unset=True)
    for key,value in update_data.items():
        setattr(user_exist,key,value)
    
    user_exist.updated = datetime.now()

    db.commit()
    db.refresh(user_exist)
    return UserResponseBase.model_validate(user_exist)
    