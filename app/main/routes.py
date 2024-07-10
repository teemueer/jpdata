from flask import render_template, send_from_directory
from app.main import bp


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")
