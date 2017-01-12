# Now I can build the views and templates to allow me to display the entries.  First I design a simple view allowing me to see all the entries.
# I made a query of Entry objects. 
from flask import render_template
from . import app
from .database import session, Entry

# I made a query of Entry objects. I order the entries by the datetime column, getting the recent ones first. 
# I used the entries.all method to retrieve all of the results. Finally I rendered a template called entries.html, passing in the list of entries.

# Here you create a new route, /page/<int:page> designed to take you to a specific page of content.
# You add an argument to your route for the page number, page, and a module constant PAGINATE_BY, which indicates how many items should be on each page.
# You then use the count method of a query object to find out how many entries there are in total.
# You can use all of this data to calculate a number of pieces of information about the pagination: start end total pages hasnext hasprev
# Then change the query so that rather than finding all entries it slices the query so you only find the entries between the start and end indices
# Finally you pass all of this information into the template
PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )
    
# Notice how you use the methods=["GET"] parameter in the route decorator. This specifies that the route will only be used for GET requests
# to the page; you will have to add a new view for the POST request which takes place when you submit the form.  
# Try visiting the /entry/add page of your app. You should see the form for adding an entry
@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")  

# Add a new route which will take your form data and create the new entry.   
# Here you create an similar route to your add_entry_get view, except this one only accepts POST requests. 
# Inside the function you create a new Entry object. You use Flask's request.form dictionary to access the data submitted with your form
# and assign it to the correct fields in the entry.

# Next you add the entry to your session, and commit it to the database. 
# Finally you use Flask's redirect function to send the user back to the front page once their entry has been created.
# Visit the /entry/add page and submit a new entry
from flask import request, redirect, url_for

@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))


@app.route("/entry/<id>")
def single_entry(id):
    single = session.query(Entry).get(id) # query will always take a class of the table your searching through
    return render_template("single.html")
    

        