import os
from app import create_app, db
from app.users.model import User

app = create_app(os.environ.get("FLASK_ENV", "default"))

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
    }
