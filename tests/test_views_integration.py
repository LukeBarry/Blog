import os
import unittest
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

# Here you use the environment variable trick to use the testing configuration. You then create a test client using the app.test_client function. 
# This will allow you to make requests to views and inspect the responses you get from the app. Next you call the Base.metadata.create_all function
# to create tables in the test database. Finally you create an example user and add it to the database. You'll use the user to log in and be the 
# author of the test entry.
from blog import app
from blog.database import Base, engine, session, User, Entry

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = User(name="Alice", email="alice@example.com",
                         password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

# Now, in the TestViews class, add a method to simulate logging in, and a test which attempts to add a entry.   

# The simulate_login method essentially mimics what Flask-Login looks for when determining whether a user is logged in. 
# You use the self.client.session_transaction method to get access to a variable representing the HTTP session. 
# You then add two variables to this session: the id of the user and a variable which tells Flask-Login that the session is still active (_fresh).   
    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

# In the test_add_entry method you call your simulate_login method so you can act as a logged in user. Then you send a POST request to
# /entry/add using the self.client.post method.You use the data parameter to provide the form data for an example entry.

# Next you start to check that the response from the app looks correct. Make sure that your user is being redirected to the / route by checking 
# the status code and location header of the response.

# Then check to make sure that the entry has been added to the database correctly. Look to see that only one entry has been added, 
# and make sure that the title, content and author are set to the correct values.

# Try running the test using PYTHONPATH=. python tests/test_views_integration.py. You should see that the entry is correctly added to the database.
    def test_add_entry(self):
        self.simulate_login()

        response = self.client.post("/entry/add", data={
            "title": "Test Entry",
            "content": "Test content"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.author, self.user)        
        
    def test_add_entry_not_authenticated(self): 
        response = self.client.get("/entry/add")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/login")
        
    def test_delete_entry(self): 
        self.simulate_login()
        
        user1 = User(name="Jared", email="example@gmail.com", password="password")
        user2 = User(name="Anne", email="example123@gmail.com", password="password")
        
        entry1 = Entry(title="Entry1", content="Some content", author_id=1)
        entry2 = Entry(title="Entry2", content="Some content", author_id=1)
        
        session.add_all([user1, user2, entry1, entry2])
        session.commit()
        
        response = self.client.post("/entry/2/delete")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        
        entry = session.query(Entry).filter(Entry.title == 'Entry2').first()
        
        self.assertEqual(entry, None)
        
    def test_delete_entry_not_author(self): 
        self.simulate_login()
        
        user1 = User(name="Jared", email="example@gmail.com", password="password")
        user2 = User(name="Anne", email="example123@gmail.com", password="password")
        
        entry1 = Entry(title="Entry1", content="Some content", author_id=2)
        entry2 = Entry(title="Entry2", content="Some content", author_id=2)
        
        session.add_all([user1, user2, entry1, entry2])
        session.commit()
        
        response = self.client.get("/entry/2/delete")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")    
        
        

if __name__ == "__main__":
    unittest.main()