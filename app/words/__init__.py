from flask import Blueprint

bp = Blueprint("words", __name__)

from . import routes
