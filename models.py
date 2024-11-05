from sqlalchemy import Boolean,Column,Integer,String,Date,ForeignKey,Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=False)
    password = Column(String,nullable=False)
    email = Column(String,unique=True,index=True,nullable=False)
    phone_number = Column(String(10),nullable=True)
    created = Column(Date,nullable=False,default=datetime.now())
    updated = Column(Date,nullable=False,default=datetime.now(),onupdate=datetime.now())
    staff = Column(Boolean,default=False,nullable=False)
    is_active = Column(Boolean,default=True)
    
    #relationships
    orders = relationship("Order",back_populates="user",cascade="all, delete-orphan")
    billing_address = relationship("BillingAddress",back_populates="user",cascade="all, delete-orphan")
    message = relationship("Message",back_populates="user",cascade="all, delete-orphan")
    
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer,primary_key=True,index=True)
    product_id = Column(String(255),nullable=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE"))
    order_date = Column(Date,nullable=False)
    total_amount = Column(Integer,nullable=False)
    
    #relationship
    user = relationship("User",back_populates="orders")
    
class BillingAddress(Base):
    __tablename__ = "billingAddresses"
    
    book_id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id',ondelete="CASCADE",onupdate="CASCADE"))
    addresse1 = Column(String(100))
    addresse2 = Column(String(100),nullable=True)
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(50))
    country = Column(String(50))
    
    #relationships
    user = relationship("User",back_populates="billing_address")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASADE",onupdate="CASCADE"))
    message_content = Column(Text,nullable=True)
    title = Column(String(100))
    date = Column(Date,nullable=False)
    
    user = relationship("User", back_populates='message')
    
    
    
    
    
    
    
    
    
    