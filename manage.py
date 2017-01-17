# Call the app.run method to start your development server.
# This file will contain a series of commands intended to help me as I develop the application.
# I could specify a command-line interface for the file using the argparse module,
# but the Flask-Script module speeds things up. Flask-Script is designed to easily specify tasks to manage the app.

# First I import the Manager object, and create an instance of it. 
# Then I add a command to the manager by decorating a function
# The name of the function corresponds with the name of the argument which I gave the manage script
# For example, to call the run function I use python manage.py run.
# Inside the run function, I try to retrieve a port number from the evironment, falling back to port 8080 if it is unavailable
# I then run the development server, telling it to listen on that port. 
# A number of hosts use the PORT environment variable to tell the app which port it should be listening on,
# so it is generally good practice for me to comply with this. Finally in the main block I run the manager.
import os
from flask.ext.script import Manager
from blog import app
from blog.database import session, Entry

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Adding a task to the manage.py file that will generate a series of entries.  
# I create a command called seed which will loop through 25 entries. In the loop I create a new entry and add it to the session.
# Finally I use the session.commit function to synchronize the changes with the database.
# I can use python manage.py seed to run the command and see the entries.
@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
    in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt 
    mollit anim id est laborum."""
    for i in range(25):
        entry=Entry(
            title="Test Entry #{}".format(i),
            content=content)
        session.add(entry)
    session.commit()
        

# Here I ask the user for their name, email address, and their password twice. 
# I check to make sure that the user is not already stored in the database, and I make sure that the passwords match.
# Then I create the user object and add it to the database.
# I use the generate_password_hash function from Werkzeug in order to hash the password.
# Hashing is a process which converts the plain text password to a string of characters, for example the string 
# baseball is converted to the hash a2c901c8c6dea98958c219f6f2d038c44dc5d362 using the SHA1 hashing algorithm.
from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.database import User

@manager.command
def adduser():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    password_2 = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()
    
    
    
    
        
        
        

        
        
        
        
if __name__ == "__main__":
    manager.run()

    
    