# Now that I have the app running, I configure the app.  
# I use the DevelopmentConfig class to contain the configuration variables which control the Flask app.
# I turn on flask's debug mode and set the location of the postgresql database.
import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/blogful"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))

# Here you have a separate database URI for testing, and you use a different secret key. You also turn off the debug setting. 
# This means that you will be testing exactly what your clients will see in production without the additional debugging information 
# (which isn't helpful within a testing environment). Go ahead and create the new test database by running createdb blogful-test. 
# (Don't forget that connection errors on port 5432 can usually be solved with sudo service postgresql start.)
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/blogful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
    
class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/blogful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"    

# The secret_key is used to cryptographically secure my application's sessions. However, it's not a good idea to store
# your application's secret key inside the application configuration itself. Therefore, I use os.environ.get to obtain 
# the secret key from an environment variable, falling back on a key generated at random on startup


    


