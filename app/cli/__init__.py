from flask import Blueprint

bp = Blueprint("cli", __name__, cli_group=None)

from . import character, decomp, heisig, dictionary