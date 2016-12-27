from flask import render_template
from . import app
from .database import session, Entry
from flask import request, redirect, url_for

PAGINATE_BY = 10 # a module constant PAGINATE_BY, which indicates how many items should be on each page (FYI - an ALL_UPPERCASE_NAME is a constant)

# Here you construct a query of Entry objects
@app.route("/")
@app.route("/page/<int:page>") # Here you create a new route, /page/<int:page> designed to take you to a specific page of content
def entries(page=1): 
    # Zero-indexed page
    page_index = page - 1
    # You add an argument to your route for the page number, page, and a module constant PAGINATE_BY

    count = session.query(Entry).count() # You then use the count method of a query object to find out how many entries there are in total

# You can use all of this data to calculate a number of pieces of information about the pagination
    start = page_index * PAGINATE_BY 
    end = start + PAGINATE_BY 
    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    
# Here you construct a query of Entry objects. You order the entries by the datetime column, getting the most recent ones first.
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end] 
# Then change the query so that rather than finding all entries it slices the query 
# so you only find the entries between the start and end indices

    return render_template("entries.html", # Finally you render a template called entries.html,
        entries=entries, #  passing in the list of entries
        has_next=has_next,# you pass all of this information into the template
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

# Allows you to view a single entry
# Should be accessed by clicking on the title of an entry
# Should use the render_entry macro to display the entry 
@app.route("/entry/<id>")
def single_entry(id):
    entry = session.query(Entry).filter(Entry.id==id).first()
    return render_template("single_entry.html", entry=entry)    


# create a view in views.py so that you can display the add_entry.html form  
# Notice how you use the methods=["GET"] parameter in the route decorator
# This specifies that the route will only be used for GET requests to the page; 
# you will have to add a new view for the POST request which takes place when you submit the form.
@app.route("/entry/add", methods=["GET"]) 
def add_entry_get(): 
    return render_template("add_entry.html")

# Add a new route which will take your form data and create the new entry.  
# Here you create a similar route to your add_entry_get view, 
# except this one only accepts POST requests. Inside the function you create a new Entry object.
# You use Flask's request.form dictionary to access the data submitted with your form 
# and assign it to the correct fields in the entry.
@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))   
    
# Next you add the entry to your session, and commit it to the database. 
# Finally you use Flask's redirect function to send the user back to the front page once their entry has been created. 
    
    '''
@app.route("/entry/<id>")
def single_entry(id):
    content = session.query(Entry).get(id)
    return render_template("add_entry.html")
       ''' 
    
    