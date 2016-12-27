import os
class DevelopmentConfig(object):  # You use this class to contain the configuration variables which control the Flask app
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/blogful"  # set the location of your database
    DEBUG = True  # You tell Flask to use its debug mode to help you track down any errors in your application
    
    
    