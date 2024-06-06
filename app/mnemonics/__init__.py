from flask import Blueprint

bp = Blueprint("mnemonics", __name__)

from . import routes
