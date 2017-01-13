# Now that I have the app running, I configure the app.  
# I use the DevelopmentConfig class to contain the configuration variables which control the Flask app.
# I turn on flask's debug mode and set the location of the postgresql database.
import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/blogful"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))

# The secret_key is used to cryptographically secure my application's sessions. However, it's not a good idea to store
# your application's secret key inside the application configuration itself. Therefore, I use os.environ.get to obtain 
# the secret key from an environment variable, falling back on a key generated at random on startup


    


