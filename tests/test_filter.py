import os
import unittest
import datetime

#Configure your app to use the testing configuration
if not "CONFIG_PATH" in os.environ: 
    os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

# The body of the code creates the FilterTests class to hold your tests, and then runs the tests in the main block. 
# The one new idea here is that you set the CONFIG_PATH environment variable to point to a TestingConfig class. 
# You might remember how in the __init__.py file you configured the Flask app based upon the value held in this environment variable.
import blog
from blog.filters import *

# The first test creates a datetime.date object, runs it through the dateformat function and makes sure that the resulting string is correct. 
# The second test passes None into the function, and makes sure that you get a None object back in return.

# Try running your tests using PYTHONPATH=. python tests/test_filters.py. You should see that the tests pass fine. 
# Notice how when you run your tests you have to set the PYTHONPATH environment variable. 
# This is so the tests can import the blog module correctly, even though it is in a different location to the test files.
class FilterTests(unittest.TestCase):
    def test_date_format(self):
        # Tonight we're gonna party...
        date = datetime.date(1999, 12, 31)
        formatted = dateformat(date, "%y/%m/%d")
        self.assertEqual(formatted, "99/12/31")

    def test_date_format_none(self):
        formatted = dateformat(None, "%y/%m/%d")
        self.assertEqual(formatted, None)

if __name__ == "__main__":
    unittest.main()