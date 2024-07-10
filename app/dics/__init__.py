from flask import Blueprint

bp = Blueprint("dics", __name__)

from . import routes
