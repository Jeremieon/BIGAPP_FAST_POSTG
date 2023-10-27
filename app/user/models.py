#import necessary modules
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from app.db import Base
from . import hashing

#define User table object
class User(Base):
    #table name
    __tablename__ ="users"

    #table objects
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    cart = relationship("Cart", back_populates="user_cart")
    order = relationship("Order", back_populates="user_info")
    tasks = relationship("TaskDB", back_populates="owner")

    #initialize user table
    def __init__(self,name,email,password,*args,**kwargs):
        self.name = name
        self.email = email
        #hash the password 
        self.password = hashing.get_password_hash(password)

    #confirm is the password is correct
    def check_password(self,password):
        return hashing.verify_password(self.password,password)
