from sqlalchemy import create_engine # basic boilerplate code for working with a database using SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"]) # create the engine which will talk to the database at the database URI which you specified in the config
Base = declarative_base() # You then create a declarative base
Session = sessionmaker(bind=engine) # and start a new session
session = Session()


# The first step is to create a SQLAlchemy model which you'll use to store and retrieve blog entries
import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

class Entry(Base): # create a new class which inherits from the declarative base object
    __tablename__ = "entries" # Give the model a table name, and add a series of columns

    id = Column(Integer, primary_key=True) # These store a primary key id, 
    title = Column(String(1024))           # the title of the entry, 
    content = Column(Text)                 # the entry content, 
    datetime = Column(DateTime, default=datetime.datetime.now) # and the date and time at which the entry was created

Base.metadata.create_all(engine) # use the Base.metadata.create_all function to construct the table in the database


