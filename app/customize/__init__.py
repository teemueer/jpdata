from flask import Blueprint

bp = Blueprint("customize", __name__)

from . import routes
