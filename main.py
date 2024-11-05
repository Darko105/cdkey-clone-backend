from fastapi import FastAPI #,HTTPException,Depends,status
# from pydantic import BaseModel
# from typing import Annotated,Optional
# import helpers
import models
from database import engine #, SessonLocal
# from sqlalchemy.orm import Session
# from datetime import datetime

from routes.users import router as user_router
from routes.addresses import router as addresses_router

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(addresses_router)



        

    
        
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



