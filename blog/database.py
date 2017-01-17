# Now that the app is configured, I setup a connection to the database where I will be storing the blog entries.
# This is the basic boilerplate code for working with a SQLAlchemy database. 
# I create the engine which will talk to the database at the database URI which I specified in the config.
# I then create a declarative base, and start a new session.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Next I use the structure I've built to start constructing the blog engine.	
# First, I create a SQLAlchemy model which I will use to store and retrieve blog entries.
# I create a new class which inherits from the declarative base object.
# Then I give the model a table name, and add a series of columns
# These columns store a primary key id, the title of the entry, the entry content, and the date and time at which the entry was created.
# Then I use the Base.metadata.create_all function to construct the table in the database.

import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)

Base.metadata.create_all(engine)


# Here I create the User model which inherits from the declarative base. 
# It also inherits from Flask-Login's UserMixin class, which adds a series of default methods. 
# Flask-Login relies on these default methods to make authentication work.Flask.
# The model has four columns: an integer id, a name, a unique email address which you will use to identify the user, and a password.
from flask.ext.login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    



















