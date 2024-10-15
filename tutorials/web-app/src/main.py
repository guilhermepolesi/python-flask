# Importing necessary modules and classes from Flask and other packages
# Flask: The core of the application
# redirect: Redirects the user to another route
# url_for: Dynamically builds URLs for the given function
# render_template: Renders an HTML template using Jinja2
# request: Handles the incoming data from HTTP requests (e.g., form data)
# session: Manages user sessions, allowing data to persist between requests
# flash: Displays one-time messages to the user (like notifications)
# test_bp: A Blueprint for managing admin routes (imported from another module)
# timedelta: Defines a duration, used here for setting session lifetime
# SQLAlchemy: A SQL ORM to interface with the SQLite database
from flask import Flask, redirect, url_for, render_template, request, session, flash
from test_blueprint import test_bp
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# Create an instance of the Flask application
app = Flask(__name__)

# Registering a blueprint for admin-related routes
# This blueprint is defined in another module (test_blueprint.py)
# All routes in the blueprint will be prefixed with "/admin"
app.register_blueprint(test_bp, url_prefix="/admin")

# Setting a secret key for securely signing the session cookie
# This is crucial for session management and data integrity
app.secret_key = "hello"

# Configuring the SQLite database with SQLAlchemy
# The database file is called 'users.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

# Disabling modification tracking for better performance
# SQLAlchemy does not need to track changes to objects unless explicitly told
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Setting the session lifetime to 5 minutes for permanent sessions
# After this duration, the session will expire automatically
app.permanent_session_lifetime = timedelta(minutes=5)

# Initialize SQLAlchemy with the Flask application
db = SQLAlchemy(app)

# Defining a model for the 'Users' table in the SQLite database
# The table will store user information (name and email)
class Users(db.Model):
    # Defining the table columns:
    # _id: The primary key, an integer that auto-increments
    # name: A string column to store the user's name
    # email: A string column to store the user's email
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    # Constructor method for creating new instances of the 'Users' model
    # It takes a name and email as input and assigns them to the instance
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Defining the root route ('/') of the application
# When the user accesses the home page, it renders the 'index.html' template
@app.route("/")
def home():
    return render_template("index.html")

# Defining the '/view' route, which displays all users in the database
# The 'view.html' template will receive the list of users as 'values'
@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())

# Defining the '/login' route, which handles both GET and POST requests
# Users can submit their name via a form, which is processed in POST requests
@app.route("/login", methods=["POST", "GET"])
def login():
    # If the request method is POST, the form has been submitted
    if request.method == "POST":
        # Setting the session to permanent, meaning it will last 5 minutes
        session.permanent = True
        # Retrieving the name submitted in the form (from 'name' input field)
        user = request.form["nm"]
        # Storing the user name in the session for future requests
        session["user"] = user

        # Checking if the user already exists in the database
        found_user = Users.query.filter_by(name=user).first()
        if found_user:
            # If the user is found, store their email in the session
            session["email"] = found_user.email
        else:
            # If the user is not found, create a new user with the name
            # Email is initially set to an empty string
            usr = Users(user, "")
            # Add the new user to the database and commit the transaction
            db.session.add(usr)
            db.session.commit()

        # Display a flash message indicating a successful login
        flash("Login Successful!")
        # Redirect the user to the 'user' route
        return redirect(url_for("user"))
    else:
        # If the user is already logged in (their name is in the session)
        if "user" in session:
            # Flash a message informing the user they're already logged in
            flash("Already Logged In!")
            # Redirect to the 'user' route
            return redirect(url_for("user"))

        # If the user is not logged in, render the login form template
        return render_template("login.html")

# Defining the '/user' route, which allows logged-in users to update their email
# This route handles both GET (display the form) and POST (submit the form)
@app.route("/user", methods=["POST", "GET"])
def user():
    # Initialize the email variable as None (will be populated if available)
    email = None
    # Check if the user is logged in (their name exists in the session)
    if "user" in session:
        user = session["user"]

        # If the request method is POST, the user submitted the form
        if request.method == "POST":
            # Retrieve the submitted email from the form
            email = request.form["email"]
            # Store the email in the session for future requests
            session["email"] = email
            # Find the user in the database and update their email
            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()  # Save the changes to the database
            # Flash a message indicating the email was saved
            flash("Email was saved!")
        else:
            # If it's a GET request and the email is in the session, load it
            if "email" in session:
                email = session["email"]

        # Render the 'user.html' template, passing the email as a variable
        return render_template("user.html", email=email)
    else:
        # If the user is not logged in, flash a warning message
        flash("You are not logged in!")
        # Redirect to the login page
        return redirect(url_for("login"))

# Defining the '/logout' route to log out the user
@app.route("/logout")
def logout():
    # If the user is logged in, display a logout flash message
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")

    # Remove the user's name and email from the session, effectively logging out
    session.pop("user", None)
    session.pop("email", None)

    # Redirect the user back to the login page
    return redirect(url_for("login"))

# Main entry point of the application
if __name__ == "__main__":
    # Ensure the application context is active to access database-related functionality
    with app.app_context():
        # Create all tables in the database (if they do not exist yet)
        db.create_all()

    # Run the Flask application in debug mode, which provides detailed error messages
    app.run(debug=True)
