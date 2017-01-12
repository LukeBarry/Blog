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
        
if __name__ == "__main__":
    manager.run()

    
    