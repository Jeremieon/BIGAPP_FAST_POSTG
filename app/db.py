#import all database dependencies
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config

#database credentials
DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = config.DATABASE_NAME

#connect to database
SQLALCHEMY_DATABASE_URL =f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

#create database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#create Database session
Sessiondb = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#create a base for database
Base = declarative_base()

#get database session
def get_db():
    db =Sessiondb()
    try:
        yield db
    finally:
        db.close()