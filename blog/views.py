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

@app.route("/")
@app.route("/page/<int:page>", methods = ["POST", "GET"])
def entries(page=1):
    print(request.args)
    if request.method=="POST":
        print(request.form)
        
    # Get the limit from the URL and convert it to an integer
    limit = request.args.get('limit', 10)
    
    # Make sure the limit is a positive integer
    try:
        limit = int(limit)
        limit = abs(limit)
    except ValueError:
        limit = 10
    
    # Make sure the limit is greater than zero
    try:
        1/int(limit)
    except ZeroDivisionError:
        limit = 10
    
    if limit > 100:
        limit = 100    
        
    paginate_by = limit    
    
    # Zero-indexed page
    page_index = page - 1
    
    count = session.query(Entry).count()
    
    start = page_index * paginate_by
    end = start + paginate_by
    total_pages = (count - 1) // paginate_by + 1
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
        total_pages=total_pages,
        limit=limit,
        count=count
    )


# Notice how you use the methods=["GET"] parameter in the route decorator. This specifies that the route will only be used for GET requests
# to the page; you will have to add a new view for the POST request which takes place when you submit the form.  
# Try visiting the /entry/add page of your app. You should see the form for adding an entry

@app.route("/entry/<id>")
def single_entry(id):
    entry = session.query(Entry).get(id) # query will always take a class of the table your searching through
    return render_template("single.html", entry=entry)


from flask.ext.login import login_required

@app.route("/entry/add", methods=["GET"])
#@login_required
def add_entry_get(): 
    if (current_user.is_authenticated): 
        return render_template("add_entry.html")
    else: 
        return redirect(url_for("login_get"))

# Add a new route which will take your form data and create the new entry.   
# Here you create an similar route to your add_entry_get view, except this one only accepts POST requests. 
# Inside the function you create a new Entry object. You use Flask's request.form dictionary to access the data submitted with your form
# and assign it to the correct fields in the entry.

# Next you add the entry to your session, and commit it to the database. 
# Finally you use Flask's redirect function to send the user back to the front page once their entry has been created.
# Visit the /entry/add page and submit a new entry
from flask import request, redirect, url_for
from flask.ext.login import current_user

@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user # Here you use the current_user variable from Flask-Login to set the author attribute when you create the entry
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))

    
@app.route("/entry/<id>/edit", methods = ["GET"])
#@login_required
def edit_entry_get(id):
    entry = session.query(Entry).get(id)
    if (current_user.is_authenticated and current_user == entry.author): 
        return render_template("edit_entry.html", entry=entry)
    elif (current_user.is_authenticated and current_user != entry.author):
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for("entries"))
    else: 
        return redirect(url_for("login_get"))

@app.route("/entry/<id>/edit", methods = ["POST"])
@login_required
def edit_entry_post(id):
    entry = session.query(Entry).get(id)
    entry.title=request.form["title"]
    entry.content=request.form["content"]
    session.commit()
    return redirect(url_for("entries"))   

@app.route("/entry/<id>/delete", methods = ["GET"])
#@login_required
def delete_entry_get(id): 
    entry = session.query(Entry).get(id)
    if (current_user.is_authenticated and current_user == entry.author): 
        return render_template("delete_entry.html", entry=entry)
    elif (current_user.is_authenticated and current_user != entry.author):
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for("entries"))
    else: 
        return redirect(url_for("login_get"))

@app.route("/entry/<id>/delete", methods = ["POST"])
@login_required
def delete_entry_post(id): 
    entry = session.query(Entry).get(id)
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))     
    
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

# Here you read the email address and password which the user entered from the request.form dictionary. 
# Next you query to find the user object with the matching email address. You check that the user exists, 
# and use Werkzeug's check_password_hash function to compare the password the user entered with the hash stored in the database.

# If the username or password is incorrect you use Flask's flash function to store a message which you can use when you render the next page. 
# In the next section you will look at how to display these messages to the user. You then redirect the user back to the login page.

# If the username and password are correct then you call Flask-Login's login_user function. This sends a cookie (a small chunk of data)
# to the user's browser which is used to identify the user. When the user then tries to access a protected resource, 
# Flask-Login will make sure that they have the cookie set and are allowed to access the resource.

# Finally when the user is logged in you redirect the user. Normally you redirect the user to the entries page. 
# However if there is a next parameter in the URL's query string then you redirect to that address. 
# Flask-Login uses this so that the user can access the intended resource after logging in.

# For example imagine that the /entry/add resource requires us to login. 
# When you visit /entry/add Flask-Login will redirect you to /login?next=/entry/add. 
# You then log in, and the view will read the next parameter and send us on to /entry/add, complying with the initial request.    
from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from .database import User
from flask.ext.login import logout_user

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))
    
@app.route("/logout")
def logout(): 
    logout_user(); 
    flash('You were logged out')
    return redirect(url_for("entries"))



