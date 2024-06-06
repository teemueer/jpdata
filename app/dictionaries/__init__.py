from flask import Blueprint

bp = Blueprint("dictionaries", __name__)

from . import routes
