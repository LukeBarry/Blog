# Here I am creating a function which takes two arguments: the date which is piped in from the template, and a format string which 
# I provide as an argument. I check to make sure I have a date object, then I use the strftime method to format the date correctly.

from . import app
from flask import Markup
import mistune as md

@app.template_filter()
def markdown(text):
    return Markup(md.markdown(text,escape=True))

@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    return date.strftime(format)
    
