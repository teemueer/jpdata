from flask import Blueprint

bp = Blueprint("characters", __name__)

from . import routes
