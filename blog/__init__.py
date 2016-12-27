import os
from flask import Flask # import the flask object

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig") # load the configuration
app.config.from_object(config_path) # you're trying to get an environment variable which will set the path to your configuration object

# Notice how these imports come after you create the app rather than at the top of the file as usual. 
# This is because the views.py and filters.py files will both make use of the app object

from . import views  # import the (currently non-existent) views and Jinja filters
from . import filters  # short-hand for import blog.views and import blog.filters
