# Here you do a couple of things. First you create an instance of the LoginManager class from Flask-Login, and initialize it. 
# Next you set a couple of attributes of the object. The login_view is the name of the view which an unauthorized user will be redirected to
# when they try to access a protected resource. The login_message_category is a category used to classify any error messages from Flask-Login.
# You will use this in conjunction with Bootstrap's alerts system to give the user information about the login process.
# Finally you create a function which tells Flask-Login how to access an object representing a user via their ID.
from flask.ext.login import LoginManager
from . import app
from.database import session, User

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_get"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))
    
    