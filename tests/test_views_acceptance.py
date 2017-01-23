import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = User(name="Alice", email="alice@example.com",
                         password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

        self.process = multiprocessing.Process(target=app.run,
                                               kwargs={"port": 8080})
        self.process.start()
        time.sleep(1)


    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()
        
    def test_login_correct(self):
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")

    def test_login_incorrect(self):
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/login")        
        
    def test_add_entry(self): 
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.browser.click_link_by_text("Add Entry")
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/entry/add")
        self.browser.fill("title", "Test Title")
        self.browser.fill("content", "Test Content")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")
                

if __name__ == "__main__":
    unittest.main()
    
''' Quite a bit of this is the same as your class in tests/test_views_integration.py. There are a couple of key differences though. 
Firstly rather than creating a test_client instance you create an instance of the splinter.Browser class, telling it to use the PhantomJS driver. 
This is what you will use for your browser automation.

The second key difference is that you use the multiprocessing module in order to start the Flask test server running. Because the test will be
visiting the actual site you need a server up to run your app.

Up until now, you've always run your app from the command line. Now, you're essentially doing the same thing, but from your python script. 
The multiprocessing module gives you the ability to start and run other code simultaneously with your own scripts. It also allows you to 
communicate and control this code, by calling methods such as start and terminate.

multiprocessing is a powerful python module – it provides features for implementing concurrency in your applications – 
which is a complicated topic all by itself. However, you don't have to understand all the underlying concepts behind concurrency 
in order to use multiprocessing. If you can understand how to create a Process object and control it using its start and terminate methods, 
that's all the knowledge you need for now.

In your test, you can't just call the app.run method as usual, because this method is blocking, and will stop the tests from running after 
it has started. So instead you launch the app.run function in a separate process.

In order to make this happen you create an instance of multiprocessing.Process. The target tells it which function to run; in this case your 
app.run method. You then start the process using its start method. Then you need to wait a little for the server to start, so you use 
time.sleep(1) in order to pause for a second.

In the teardown method you kill the server using the Process.terminate method, and make the browser exit using the Browser.quit method.

Now you can add a couple of tests to your class which use the browser object to check that the login system works.    

The tests are both very similar, they just use different data for a correct and incorrect login. First you visit the login page using 
the Browser.visit method. You then fill in the form fields using the Browser.fill method. This looks for an <input> element within the HTML
which has a name attribute matching the first argument. In this case you are looking for the email and password fields. 
It then fills these in with the information given in the second argument.

Next you find the submit button on the page using the Browser.find_by_css method. This uses css selector rules to find an item on the page. 
In this case you look for a <button> element which has the type attribute set to "submit". Next you use the click method to submit the form. 
Finally you check to make sure that you have been relocated to the correct location: the front page if you have logged in successfully, 
or back to the login page if the information you gave was incorrect.

Try running these tests using PYTHONPATH=. python tests/test_views_acceptance.py. In the background Selenium will run through the actions 
which you have specified as if they were being performed on a regular browser, by an end user. You will then be given the results of the tests.

Notice how (whilst being much more interesting to watch) these tests take significantly longer to run than the unit and integration tests. 
You have something of a trade-off:

Unit tests run very quickly but only give you information about isolated sections of your code
Integration tests run a little less quickly, and give you information about how different elements are working together
Acceptance tests run slower still, but give you information that your whole system is working correctly
In larger projects you will need to carefully manage the balance between the different types of tests, choosing the appropriate style of 
testing for the problem you are tackling. In practice you often need to use a combination of the three styles in order to have well tested 
and maintainable code.

'''

