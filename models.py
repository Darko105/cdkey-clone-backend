from sqlalchemy import Boolean,Column,Integer,String,Date,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=False)
    password = Column(String(255),nullable=False)
    email = Column(String(255),nullable=False)
    phone_number = Column(String(255),nullable=True)
    created = Column(Date,nullable=False)
    updated = Column(Date,nullable=False)
    staff = Column(Boolean,nullable=False)
    
    #relationships
    orders = relationship("Order",back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer,primary_key=True,index=True)
    product_id = Column(String(255),nullable=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    order_date = Column(Date,nullable=False)
    total_amount = Column(Integer,nullable=False)
    
    #relationship
    user = relationship("User",back_populates="orders")
    
    
    
    
    
    