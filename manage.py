import os
from flask.ext.script import Manager  # Flask-Script is designed to allow you to easily specify tasks to help you manage your application

from blog import app  # Get the app function from the __init__.py file

manager = Manager(app)  # First you import the Manager object, and create an instance of it

@manager.command  # Then you add a command to the manager by decorating a function
def run():  # The name of the function corresponds with the name of the argument 
            # which you give the manage script. For example to call the run function you'll say python manage.py run
    port = int(os.environ.get('PORT', 8080))  
    app.run(host='0.0.0.0', port=port)   
     
# Inside the run function you try to retrieve a port number from the environment,
# falling back to port 8080 if it is unavailable. You then run the development server,
# telling it to listen on that port. A number of hosts use the PORT environment variable
# to tell the app which port it should be listening on, so it is generally good practice to comply with this     


# Add a task to your manager which will generate a series of entries
from blog.database import session, Entry

@manager.command
def seed(): # Here you create a command called seed which will add a series of entries to the database
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    # In the seed function you create a string of dummy text for the entry content
    for i in range(25): # You then run a loop 25 times
        entry = Entry( #  In the loop you create a new entry and add it to the session
            title="Test Entry #{}".format(i),
            content=content
        )
        session.add(entry) 
    session.commit() # Finally you use the session.commit function to synchronize our changes with the database

if __name__ == "__main__":  # Finally in the main block you run the manager
    manager.run()  
    
# Try using this script to launch the development server by saying python manage.py run. 
#  You should see the server launched as usual listening on port 8080.
    