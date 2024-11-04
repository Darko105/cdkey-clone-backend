from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated,Optional
import helpers
import models
from database import engine, SessonLocal
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserCreateBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    password: str
    staff: bool
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

class UserResponseBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    staff: bool
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True
        
        
# Dummy : Route to create a user
# @app.post("/users/", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     hashed_password = hash_password(user.password)
#     db_user = models.User(
#         first_name=user.first_name,
#         last_name=user.last_name,
#         email=user.email,
#         phone_number=user.phone_number,
#         staff=user.staff,
#         password=hashed_password,
#         created=datetime.utcnow(),
#         updated=datetime.utcnow()
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def get_db():
    db = SessonLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session, Depends(get_db)]

@app.post("/users/",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateBase, db:db_dependency):
    user_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already exist.!")
    
    hashed_password = helpers.hash_password(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email, 
        phone_number=user.phone_number,
        staff=user.staff,
        password=hashed_password,
        created=datetime.utcnow(),
        updated=datetime.utcnow()
    )
    
  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponseBase.model_validate(db_user)

@app.get("/users/{user_id}",status_code=status.HTTP_200_OK)
async def get_user(user_id:int,db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User Not Found!")
    return UserResponseBase.model_validate(user)


