# From macros.html You're using the markdown filter on the entry content. This allows you to use the Markdown syntax, 
# making it simpler to write well-formatted blog entries. You use the dateformat filter to display
# the datetime in dd/mm/yy format. Jinja doesn't include these filters by default 
# so you need to add the filters.py file

from . import app
from flask import Markup
import mistune as md

# Here you're creating a function which takes two arguments: 
# the date which is piped in from the template, and a format string which you provide as an argument
# Check to make sure that you have a date object, 
# then you use the strftime method to format the date correctly.
@app.template_filter()
def markdown(text):
    return Markup(md.markdown(text,escape=True))

@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    return date.strftime(format)
    
# The final step towards viewing the entries is to actually add the entries.html template:    