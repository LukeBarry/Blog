# Now that I have the app running, I configure the app.  
# I use the DevelopmentConfig class to contain the configuration variables which control the Flask app.
# I turn on flask's debug mode and set the location of the postgresql database.
import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/blogful"
    DEBUG = True
    
    


