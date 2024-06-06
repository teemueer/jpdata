from flask import abort
from flask_login import login_required, current_user
from app import db
from app.users import bp
from app.users.model import User

@bp.route("/users")
@login_required
def users():
    if not current_user.is_admin:
        abort(401)
    users = db.session.query(User).all()
    return users[0].to_dict()