# Importing necessary modules from Flask
# Blueprint: Used to organize routes into modules, allowing better structure for large applications
# render_template: Used to render HTML templates using Jinja2
from flask import Blueprint, render_template

# Creating a blueprint named 'test_blueprint'
# This blueprint will handle routes related to 'test' functionality
# static_folder: Specifies the folder where static files (CSS, JS) are located in the structure
# template_folder: Specifies the folder where HTML templates are stored
test_bp = Blueprint("test_blueprint", __name__, static_folder="static", template_folder="templates")

# Defining a route for '/home' and the root route ('/')
# Both routes will render the 'index.html' template when accessed
@test_bp.route("/home")
@test_bp.route("/")
def home():
    # Renders and returns the 'index.html' file located in the template folder
    return render_template("index.html")

# Defining a route for '/test'
# This route returns a simple HTML heading as a response
@test_bp.route("/test")
def test():
    # Returns a plain HTML response with the text "test"
    return "<h1>test</h1>"
