from flask import Flask, g, request
from flask_login import LoginManager
from config import config
from app.database import db, migrate

login = LoginManager()
login.login_view = "auth.login"


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.filters import register_filters

    register_filters(app)

    from app.cli import bp as cli_bp
    from app.main import bp as main_bp
    from app.characters import bp as characters_bp
    from app.dics import bp as dics_bp
    from app.auth import bp as auth_bp
    from app.mnemonics import bp as mnemonics_bp
    from app.words import bp as words_bp
    from app.customize import bp as customize_bp

    app.register_blueprint(cli_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(dics_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(mnemonics_bp)
    app.register_blueprint(words_bp)
    app.register_blueprint(customize_bp)

    @app.before_request
    def before_request():
        g.theme = request.cookies.get("theme", "light")

    return app
