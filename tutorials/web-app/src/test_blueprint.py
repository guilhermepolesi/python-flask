from flask import Blueprint, render_template

test_bp = Blueprint("test_blueprint", __name__, static_folder="static", template_folder="templates")

@test_bp.route("/home")
@test_bp.route("/")
def home():
    return render_template("index.html")


@test_bp.route("/test")
def test():
    return "<h1>test</h1>"