# Fire up the development server.  Import the flask object and create the app in the usual way.
# Import the views and Jija filters.  The views and filters imports both make use of the app object,
# which is why they come after the app object.  Another way to write those two lines import blog.views and import blog.filters
import os
from flask import Flask

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import views
from . import filters
from . import login


# After I created the config file, I came back to this file and loaded the configuration.
# Line 8 is trying to get an environment variable which will set the path to my configuration object.
# If the variable is not set then I default to my development configuration.
# This provides a way to switch between configurations easily in defferent situation;
# I can use this to switch over to a different configuration for testing the application
# Line 9 uses the app.config.from_object method to configure the app using the configuration object.

