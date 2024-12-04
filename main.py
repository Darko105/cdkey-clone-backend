from fastapi import FastAPI #,HTTPException,Depends,status
# from pydantic import BaseModel
# from typing import Annotated,Optional
# import helpers
import models
from database import engine #, SessonLocal
# from sqlalchemy.orm import Session
# from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as user_router
from routes.addresses import router as addresses_router
from routes.messages import router as messages_router
from routes.rewards import router as rewards_router
from routes.orders import router as orders_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods GET, POST, OPTIONS,
    allow_headers=["*"],  # Allow all headers
)

models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(addresses_router)
app.include_router(messages_router)
app.include_router(rewards_router)
app.include_router(orders_router)



        

    
        
# Dummy : Route to create a user test
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



